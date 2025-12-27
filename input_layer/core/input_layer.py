"""
Main Input Layer orchestrator class.
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json

from ..models.input_types import InputData, ProcessedData, InputType, ProcessingStatus
from ..handlers.competitor_handler import CompetitorHandler
from ..handlers.hashtag_handler import HashtagHandler
from ..handlers.zipcode_handler import ZipCodeHandler
from ..exceptions import InputLayerError, ValidationError, ProcessingError


class InputLayer:
    """
    Main orchestrator class for the Input Layer module.
    
    This class coordinates the processing of different types of input data
    through appropriate handlers and provides a unified interface for
    API and UI integration.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Input Layer with configuration.
        
        Args:
            config: Configuration dictionary with handler-specific configs:
                - competitor_handler: Config for CompetitorHandler
                - hashtag_handler: Config for HashtagHandler  
                - zipcode_handler: Config for ZipCodeHandler
                - global_settings: Global settings for all handlers
        """
        self.config = config or {}
        self.global_config = self.config.get("global_settings", {})
        
        # Initialize handlers
        self.handlers = {
            InputType.COMPETITOR_NAME: CompetitorHandler(
                self.config.get("competitor_handler", {})
            ),
            InputType.HASHTAG: HashtagHandler(
                self.config.get("hashtag_handler", {})
            ),
            InputType.ZIP_CODE: ZipCodeHandler(
                self.config.get("zipcode_handler", {})
            )
        }
        
        # Processing statistics
        self.stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "validation_errors": 0,
            "by_type": {
                InputType.COMPETITOR_NAME.value: {"processed": 0, "successful": 0, "failed": 0},
                InputType.HASHTAG.value: {"processed": 0, "successful": 0, "failed": 0},
                InputType.ZIP_CODE.value: {"processed": 0, "successful": 0, "failed": 0}
            }
        }
    
    def process_single(self, data: Union[str, InputData], input_type: Union[str, InputType]) -> ProcessedData:
        """
        Process a single input data item.
        
        Args:
            data: Input data (string or InputData object)
            input_type: Type of input data
            
        Returns:
            ProcessedData object with results
            
        Raises:
            InputLayerError: If input type is not supported
            ProcessingError: If processing fails
        """
        # Convert string input to InputData
        if isinstance(data, str):
            if isinstance(input_type, str):
                input_type = InputType(input_type)
            input_data = InputData(data=data, input_type=input_type)
        else:
            input_data = data
        
        # Get appropriate handler
        handler = self.handlers.get(input_data.input_type)
        if not handler:
            raise InputLayerError(f"No handler available for input type: {input_data.input_type}")
        
        try:
            # Process the data
            result = handler.process(input_data)
            
            # Update statistics
            self._update_stats(result)
            
            return result
            
        except Exception as e:
            # Update failure statistics
            self.stats["total_processed"] += 1
            self.stats["failed"] += 1
            self.stats["by_type"][input_data.input_type.value]["processed"] += 1
            self.stats["by_type"][input_data.input_type.value]["failed"] += 1
            
            raise ProcessingError(f"Failed to process {input_data.input_type.value}: {str(e)}") from e
    
    def process_batch(self, data_list: List[Union[str, InputData]], 
                     input_type: Union[str, InputType] = None) -> List[ProcessedData]:
        """
        Process multiple input data items in batch.
        
        Args:
            data_list: List of input data items
            input_type: Type of input data (if all items are strings)
            
        Returns:
            List of ProcessedData objects
            
        Raises:
            InputLayerError: If input type is not supported
        """
        results = []
        
        for data in data_list:
            try:
                # Determine input type
                if isinstance(data, str):
                    if input_type is None:
                        raise InputLayerError("input_type must be specified when processing string data")
                    result = self.process_single(data, input_type)
                else:
                    result = self.process_single(data, data.input_type)
                
                results.append(result)
                
            except Exception as e:
                # Create error result for failed items
                error_result = ProcessedData(
                    original_data=str(data),
                    processed_data="",
                    input_type=input_type if isinstance(input_type, InputType) else InputType(input_type) if input_type else InputType.COMPETITOR_NAME,
                    status=ProcessingStatus.FAILED,
                    validation_result=None,
                    metadata={"error": str(e), "processing_timestamp": datetime.now().isoformat()}
                )
                results.append(error_result)
        
        return results
    
    def process_mixed_batch(self, data_list: List[InputData]) -> List[ProcessedData]:
        """
        Process a mixed batch of different input types.
        
        Args:
            data_list: List of InputData objects with different types
            
        Returns:
            List of ProcessedData objects
        """
        results = []
        
        for data in data_list:
            try:
                result = self.process_single(data, data.input_type)
                results.append(result)
            except Exception as e:
                # Create error result for failed items
                error_result = ProcessedData(
                    original_data=data.data,
                    processed_data="",
                    input_type=data.input_type,
                    status=ProcessingStatus.FAILED,
                    validation_result=None,
                    metadata={"error": str(e), "processing_timestamp": datetime.now().isoformat()}
                )
                results.append(error_result)
        
        return results
    
    def validate_single(self, data: Union[str, InputData], input_type: Union[str, InputType] = None) -> Dict[str, Any]:
        """
        Validate a single input data item without processing.
        
        Args:
            data: Input data to validate
            input_type: Type of input data (required if data is string)
            
        Returns:
            Dictionary with validation results
            
        Raises:
            InputLayerError: If input type is not supported
        """
        # Convert string input to InputData
        if isinstance(data, str):
            if input_type is None:
                raise InputLayerError("input_type must be specified when validating string data")
            if isinstance(input_type, str):
                input_type = InputType(input_type)
            input_data = InputData(data=data, input_type=input_type)
        else:
            input_data = data
        
        # Get appropriate handler
        handler = self.handlers.get(input_data.input_type)
        if not handler:
            raise InputLayerError(f"No handler available for input type: {input_data.input_type}")
        
        # Perform validation
        validation_result = handler.validate(input_data)
        
        return {
            "is_valid": validation_result.is_valid,
            "errors": validation_result.errors,
            "warnings": validation_result.warnings,
            "suggestions": validation_result.suggestions,
            "input_type": input_data.input_type.value,
            "original_data": input_data.data
        }
    
    def get_supported_types(self) -> List[str]:
        """
        Get list of supported input types.
        
        Returns:
            List of supported input type strings
        """
        return [input_type.value for input_type in self.handlers.keys()]
    
    def get_handler_config(self, input_type: Union[str, InputType]) -> Dict[str, Any]:
        """
        Get configuration for a specific handler.
        
        Args:
            input_type: Input type to get config for
            
        Returns:
            Handler configuration dictionary
            
        Raises:
            InputLayerError: If input type is not supported
        """
        if isinstance(input_type, str):
            input_type = InputType(input_type)
        
        handler = self.handlers.get(input_type)
        if not handler:
            raise InputLayerError(f"No handler available for input type: {input_type}")
        
        return handler.config
    
    def update_handler_config(self, input_type: Union[str, InputType], config: Dict[str, Any]) -> None:
        """
        Update configuration for a specific handler.
        
        Args:
            input_type: Input type to update config for
            config: New configuration dictionary
            
        Raises:
            InputLayerError: If input type is not supported
        """
        if isinstance(input_type, str):
            input_type = InputType(input_type)
        
        handler = self.handlers.get(input_type)
        if not handler:
            raise InputLayerError(f"No handler available for input type: {input_type}")
        
        # Update handler config
        handler.config.update(config)
        
        # Reinitialize handler with new config
        if input_type == InputType.COMPETITOR_NAME:
            self.handlers[input_type] = CompetitorHandler(handler.config)
        elif input_type == InputType.HASHTAG:
            self.handlers[input_type] = HashtagHandler(handler.config)
        elif input_type == InputType.ZIP_CODE:
            self.handlers[input_type] = ZipCodeHandler(handler.config)
    
    def prompt_user_and_process(self) -> Dict[str, List[ProcessedData]]:
        """
        Interactively prompt the user for competitor names, hashtags, and ZIP codes,
        process them, print cleaned results, and return all results.
        
        Input format:
        - Competitor names: comma-separated (e.g., Acme Inc, local bakery, Big Tech)
        - Hashtags: comma-separated (e.g., #tech, innovation, Cloud_Solutions)
        - ZIP codes: comma-separated (e.g., 94102, 10001)
        
        Returns:
            Dict with keys: "competitor_names", "hashtags", "zip_codes" mapping to lists of ProcessedData.
        """
        print("\n=== Input Layer Interactive Mode ===")
        try:
            raw_names = input("Enter competitor names (comma-separated): ").strip()
        except EOFError:
            raw_names = ""
        try:
            raw_tags = input("Enter hashtags (comma-separated): ").strip()
        except EOFError:
            raw_tags = ""
        try:
            raw_zips = input("Enter ZIP codes (comma-separated): ").strip()
        except EOFError:
            raw_zips = ""

        def split_items(raw: str) -> List[str]:
            if not raw:
                return []
            return [item.strip() for item in raw.split(',') if item.strip()]

        names = split_items(raw_names)
        tags = split_items(raw_tags)
        zips = split_items(raw_zips)

        results_names: List[ProcessedData] = []
        results_tags: List[ProcessedData] = []
        results_zips: List[ProcessedData] = []

        # Process competitor names
        for name in names:
            try:
                res = self.process_single(name, InputType.COMPETITOR_NAME)
                results_names.append(res)
            except Exception as e:
                results_names.append(ProcessedData(
                    original_data=name,
                    processed_data="",
                    input_type=InputType.COMPETITOR_NAME,
                    status=ProcessingStatus.FAILED,
                    validation_result=None,
                    metadata={"error": str(e), "processing_timestamp": datetime.now().isoformat()}
                ))

        # Process hashtags
        for tag in tags:
            try:
                res = self.process_single(tag, InputType.HASHTAG)
                results_tags.append(res)
            except Exception as e:
                results_tags.append(ProcessedData(
                    original_data=tag,
                    processed_data="",
                    input_type=InputType.HASHTAG,
                    status=ProcessingStatus.FAILED,
                    validation_result=None,
                    metadata={"error": str(e), "processing_timestamp": datetime.now().isoformat()}
                ))

        # Process ZIP codes
        for z in zips:
            try:
                res = self.process_single(z, InputType.ZIP_CODE)
                results_zips.append(res)
            except Exception as e:
                results_zips.append(ProcessedData(
                    original_data=z,
                    processed_data="",
                    input_type=InputType.ZIP_CODE,
                    status=ProcessingStatus.FAILED,
                    validation_result=None,
                    metadata={"error": str(e), "processing_timestamp": datetime.now().isoformat()}
                ))

        # Pretty print results
        def summarize(items: List[ProcessedData]) -> List[str]:
            out: List[str] = []
            for r in items:
                if r.status == ProcessingStatus.COMPLETED and r.validation_result is not None:
                    out.append(r.processed_data)
                else:
                    err = r.metadata.get("error") if r.metadata else "unknown error"
                    out.append(f"[error: {err}]")
            return out

        print("\nCleaned Results:")
        print(f"  Competitor Names: {summarize(results_names)}")
        print(f"  Hashtags: {summarize(results_tags)}")
        print(f"  ZIP Codes: {summarize(results_zips)}")

        return {
            "competitor_names": results_names,
            "hashtags": results_tags,
            "zip_codes": results_zips,
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dictionary with processing statistics
        """
        return {
            "statistics": self.stats.copy(),
            "success_rate": (
                self.stats["successful"] / self.stats["total_processed"] * 100
                if self.stats["total_processed"] > 0 else 0
            ),
            "last_updated": datetime.now().isoformat()
        }
    
    def reset_statistics(self) -> None:
        """Reset processing statistics."""
        self.stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "validation_errors": 0,
            "by_type": {
                InputType.COMPETITOR_NAME.value: {"processed": 0, "successful": 0, "failed": 0},
                InputType.HASHTAG.value: {"processed": 0, "successful": 0, "failed": 0},
                InputType.ZIP_CODE.value: {"processed": 0, "successful": 0, "failed": 0}
            }
        }
    
    def export_results(self, results: List[ProcessedData], format: str = "json") -> str:
        """
        Export processing results to specified format.
        
        Args:
            results: List of ProcessedData objects
            format: Export format ("json", "csv")
            
        Returns:
            Exported data as string
            
        Raises:
            InputLayerError: If format is not supported
        """
        if format == "json":
            return json.dumps([result.to_dict() for result in results], indent=2)
        elif format == "csv":
            # Simple CSV export
            import csv
            import io
            
            output = io.StringIO()
            if results:
                writer = csv.DictWriter(output, fieldnames=[
                    "original_data", "processed_data", "input_type", "status", 
                    "is_valid", "errors", "warnings", "suggestions"
                ])
                writer.writeheader()
                
                for result in results:
                    row = {
                        "original_data": result.original_data,
                        "processed_data": result.processed_data,
                        "input_type": result.input_type.value,
                        "status": result.status.value,
                        "is_valid": result.validation_result.is_valid,
                        "errors": "; ".join(result.validation_result.errors),
                        "warnings": "; ".join(result.validation_result.warnings),
                        "suggestions": "; ".join(result.validation_result.suggestions)
                    }
                    writer.writerow(row)
            
            return output.getvalue()
        else:
            raise InputLayerError(f"Unsupported export format: {format}")
    
    def _update_stats(self, result: ProcessedData) -> None:
        """
        Update processing statistics based on result.
        
        Args:
            result: ProcessedData result to update stats with
        """
        self.stats["total_processed"] += 1
        
        if result.status == ProcessingStatus.COMPLETED:
            self.stats["successful"] += 1
        elif result.status == ProcessingStatus.VALIDATION_ERROR:
            self.stats["validation_errors"] += 1
        else:
            self.stats["failed"] += 1
        
        # Update by-type statistics
        type_stats = self.stats["by_type"][result.input_type.value]
        type_stats["processed"] += 1
        
        if result.status == ProcessingStatus.COMPLETED:
            type_stats["successful"] += 1
        else:
            type_stats["failed"] += 1
