"""
Regional analyzer for extracting geographic and demographic information from ZIP codes.
"""

import re
from typing import List, Dict, Any, Optional, Set
from collections import Counter
from datetime import datetime

from ..models.base import BaseAnalyzer
from ..models.context_types import RegionalInfo, RegionType
from ..exceptions import RegionalAnalysisError


class RegionalAnalyzer(BaseAnalyzer):
    """Analyzer for regional information from ZIP codes."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize regional analyzer with configuration.
        
        Args:
            config: Configuration dictionary with options:
                - zip_to_region_mapping: Dictionary mapping ZIP codes to regions
                - state_mappings: Dictionary mapping ZIP codes to states
                - metro_area_mappings: Dictionary mapping ZIP codes to metro areas
                - economic_indicators: Dictionary of economic indicators by region
                - demographic_indicators: Dictionary of demographic indicators by region
        """
        super().__init__(config)
        
        # Load ZIP code to region mappings
        self.zip_to_region = self.get_config_value("zip_to_region_mapping", self._get_default_zip_mappings())
        self.zip_to_state = self.get_config_value("state_mappings", self._get_default_state_mappings())
        self.zip_to_metro = self.get_config_value("metro_area_mappings", self._get_default_metro_mappings())
        
        # Economic and demographic indicators
        self.economic_indicators = self.get_config_value("economic_indicators", {})
        self.demographic_indicators = self.get_config_value("demographic_indicators", {})
        
        # Region type classifications
        self.region_type_mappings = self._get_default_region_types()
    
    def _get_default_zip_mappings(self) -> Dict[str, str]:
        """Get default ZIP code to region mappings."""
        return {
            # Major metropolitan areas
            "10001": "New York Metro", "10002": "New York Metro", "10003": "New York Metro",
            "90210": "Los Angeles Metro", "90211": "Los Angeles Metro", "94102": "San Francisco Bay Area",
            "60601": "Chicago Metro", "60602": "Chicago Metro", "60603": "Chicago Metro",
            "77001": "Houston Metro", "77002": "Houston Metro", "77003": "Houston Metro",
            "33101": "Miami Metro", "33102": "Miami Metro", "33103": "Miami Metro",
            "85001": "Phoenix Metro", "85002": "Phoenix Metro", "85003": "Phoenix Metro",
            "98101": "Seattle Metro", "98102": "Seattle Metro", "98103": "Seattle Metro",
            "02101": "Boston Metro", "02102": "Boston Metro", "02103": "Boston Metro",
            "30301": "Atlanta Metro", "30302": "Atlanta Metro", "30303": "Atlanta Metro",
            
            # Suburban areas
            "07001": "New Jersey Suburbs", "07002": "New Jersey Suburbs",
            "90210": "Beverly Hills", "90211": "Beverly Hills",
            "60001": "Chicago Suburbs", "60002": "Chicago Suburbs",
            
            # Rural/smaller areas
            "01001": "Western Massachusetts", "01002": "Western Massachusetts",
            "59001": "Montana Rural", "59002": "Montana Rural",
            "99701": "Alaska Rural", "99702": "Alaska Rural"
        }
    
    def _get_default_state_mappings(self) -> Dict[str, str]:
        """Get default ZIP code to state mappings."""
        return {
            # New York
            "10001": "NY", "10002": "NY", "10003": "NY", "07001": "NJ", "07002": "NJ",
            
            # California
            "90210": "CA", "90211": "CA", "94102": "CA", "94103": "CA",
            
            # Illinois
            "60601": "IL", "60602": "IL", "60603": "IL", "60001": "IL", "60002": "IL",
            
            # Texas
            "77001": "TX", "77002": "TX", "77003": "TX",
            
            # Florida
            "33101": "FL", "33102": "FL", "33103": "FL",
            
            # Arizona
            "85001": "AZ", "85002": "AZ", "85003": "AZ",
            
            # Washington
            "98101": "WA", "98102": "WA", "98103": "WA",
            
            # Massachusetts
            "02101": "MA", "02102": "MA", "02103": "MA", "01001": "MA", "01002": "MA",
            
            # Georgia
            "30301": "GA", "30302": "GA", "30303": "GA",
            
            # Montana
            "59001": "MT", "59002": "MT",
            
            # Alaska
            "99701": "AK", "99702": "AK"
        }
    
    def _get_default_metro_mappings(self) -> Dict[str, str]:
        """Get default ZIP code to metro area mappings."""
        return {
            "10001": "New York-Newark-Jersey City", "10002": "New York-Newark-Jersey City",
            "90210": "Los Angeles-Long Beach-Anaheim", "90211": "Los Angeles-Long Beach-Anaheim",
            "94102": "San Francisco-Oakland-Berkeley", "60601": "Chicago-Naperville-Elgin",
            "77001": "Houston-The Woodlands-Sugar Land", "33101": "Miami-Fort Lauderdale-Pompano Beach",
            "85001": "Phoenix-Mesa-Chandler", "98101": "Seattle-Tacoma-Bellevue",
            "02101": "Boston-Cambridge-Newton", "30301": "Atlanta-Sandy Springs-Alpharetta"
        }
    
    def _get_default_region_types(self) -> Dict[str, RegionType]:
        """Get default region type classifications."""
        return {
            # Major metros - Urban
            "New York Metro": RegionType.URBAN,
            "Los Angeles Metro": RegionType.URBAN,
            "San Francisco Bay Area": RegionType.URBAN,
            "Chicago Metro": RegionType.URBAN,
            "Houston Metro": RegionType.URBAN,
            "Miami Metro": RegionType.URBAN,
            "Phoenix Metro": RegionType.URBAN,
            "Seattle Metro": RegionType.URBAN,
            "Boston Metro": RegionType.URBAN,
            "Atlanta Metro": RegionType.URBAN,
            
            # Suburban areas
            "New Jersey Suburbs": RegionType.SUBURBAN,
            "Beverly Hills": RegionType.SUBURBAN,
            "Chicago Suburbs": RegionType.SUBURBAN,
            
            # Rural areas
            "Western Massachusetts": RegionType.RURAL,
            "Montana Rural": RegionType.RURAL,
            "Alaska Rural": RegionType.RURAL
        }
    
    def analyze(self, data: List[Dict[str, Any]]) -> RegionalInfo:
        """
        Analyze regional information from ZIP codes.
        
        Args:
            data: List of processed data from Input Layer
            
        Returns:
            RegionalInfo object with regional analysis
            
        Raises:
            RegionalAnalysisError: If analysis fails
        """
        self.validate_input(data)
        
        try:
            # Extract ZIP codes from data
            zip_codes = []
            for item in data:
                if item.get("input_type") == "zip_code":
                    zip_code = item.get("processed_data", "")
                    if zip_code:
                        zip_codes.append(zip_code)
            
            if not zip_codes:
                return RegionalInfo()  # Return empty info if no ZIP codes
            
            # Analyze ZIP codes
            regions = self._analyze_regions(zip_codes)
            states = self._analyze_states(zip_codes)
            metro_areas = self._analyze_metro_areas(zip_codes)
            
            # Determine primary region
            primary_region = self._determine_primary_region(regions)
            
            # Determine region type
            region_type = self._determine_region_type(primary_region, regions)
            
            # Analyze population density
            population_density = self._analyze_population_density(regions)
            
            # Get economic indicators
            economic_indicators = self._get_economic_indicators(primary_region, states)
            
            # Get demographic indicators
            demographic_indicators = self._get_demographic_indicators(primary_region, states)
            
            # Analyze geographic features
            geographic_features = self._analyze_geographic_features(regions, states)
            
            # Analyze market characteristics
            market_characteristics = self._analyze_market_characteristics(regions, region_type)
            
            return RegionalInfo(
                primary_region=primary_region,
                region_type=region_type,
                state=states[0] if states else None,
                metro_area=metro_areas[0] if metro_areas else None,
                population_density=population_density,
                economic_indicators=economic_indicators,
                demographic_indicators=demographic_indicators,
                geographic_features=geographic_features,
                market_characteristics=market_characteristics,
                zip_codes_analyzed=zip_codes
            )
            
        except Exception as e:
            raise RegionalAnalysisError(f"Regional analysis failed: {str(e)}") from e
    
    def _analyze_regions(self, zip_codes: List[str]) -> List[str]:
        """Analyze regions from ZIP codes."""
        regions = []
        
        for zip_code in zip_codes:
            # Extract 5-digit ZIP for lookup
            five_digit = self._extract_five_digit_zip(zip_code)
            if five_digit:
                region = self.zip_to_region.get(five_digit)
                if region:
                    regions.append(region)
        
        return list(set(regions))  # Remove duplicates
    
    def _analyze_states(self, zip_codes: List[str]) -> List[str]:
        """Analyze states from ZIP codes."""
        states = []
        
        for zip_code in zip_codes:
            five_digit = self._extract_five_digit_zip(zip_code)
            if five_digit:
                state = self.zip_to_state.get(five_digit)
                if state:
                    states.append(state)
        
        return list(set(states))
    
    def _analyze_metro_areas(self, zip_codes: List[str]) -> List[str]:
        """Analyze metro areas from ZIP codes."""
        metro_areas = []
        
        for zip_code in zip_codes:
            five_digit = self._extract_five_digit_zip(zip_code)
            if five_digit:
                metro = self.zip_to_metro.get(five_digit)
                if metro:
                    metro_areas.append(metro)
        
        return list(set(metro_areas))
    
    def _extract_five_digit_zip(self, zip_code: str) -> Optional[str]:
        """Extract 5-digit ZIP code from formatted ZIP."""
        # Remove spaces, dashes, and extract first 5 digits
        cleaned = re.sub(r'[-\s]', '', zip_code)
        digits = re.findall(r'\d', cleaned)
        
        if len(digits) >= 5:
            return ''.join(digits[:5])
        
        return None
    
    def _determine_primary_region(self, regions: List[str]) -> Optional[str]:
        """Determine the primary region from the list."""
        if not regions:
            return None
        
        # If only one region, return it
        if len(regions) == 1:
            return regions[0]
        
        # If multiple regions, choose the most significant one
        # Prioritize major metropolitan areas
        metro_priority = ["New York Metro", "Los Angeles Metro", "San Francisco Bay Area", 
                         "Chicago Metro", "Houston Metro", "Miami Metro"]
        
        for metro in metro_priority:
            if metro in regions:
                return metro
        
        # Return the first region if no metro area found
        return regions[0]
    
    def _determine_region_type(self, primary_region: Optional[str], all_regions: List[str]) -> Optional[RegionType]:
        """Determine the region type based on regions."""
        if primary_region:
            return self.region_type_mappings.get(primary_region)
        
        # If no primary region, check all regions
        region_types = []
        for region in all_regions:
            region_type = self.region_type_mappings.get(region)
            if region_type:
                region_types.append(region_type)
        
        if region_types:
            # Return the most common type
            from collections import Counter
            return Counter(region_types).most_common(1)[0][0]
        
        return None
    
    def _analyze_population_density(self, regions: List[str]) -> Optional[str]:
        """Analyze population density based on regions."""
        if not regions:
            return None
        
        # Simple density classification based on region type
        urban_regions = ["New York Metro", "Los Angeles Metro", "San Francisco Bay Area", 
                        "Chicago Metro", "Houston Metro", "Miami Metro", "Phoenix Metro", 
                        "Seattle Metro", "Boston Metro", "Atlanta Metro"]
        
        suburban_regions = ["New Jersey Suburbs", "Beverly Hills", "Chicago Suburbs"]
        
        rural_regions = ["Western Massachusetts", "Montana Rural", "Alaska Rural"]
        
        for region in regions:
            if region in urban_regions:
                return "High"
            elif region in suburban_regions:
                return "Medium"
            elif region in rural_regions:
                return "Low"
        
        return "Medium"  # Default
    
    def _get_economic_indicators(self, primary_region: Optional[str], states: List[str]) -> Dict[str, Any]:
        """Get economic indicators for the region."""
        indicators = {}
        
        if primary_region:
            # Add region-specific indicators
            if "New York" in primary_region:
                indicators["financial_center"] = True
                indicators["high_income"] = True
                indicators["diverse_economy"] = True
            elif "Silicon Valley" in primary_region or "San Francisco" in primary_region:
                indicators["tech_hub"] = True
                indicators["high_income"] = True
                indicators["innovation_center"] = True
            elif "Los Angeles" in primary_region:
                indicators["entertainment_hub"] = True
                indicators["diverse_economy"] = True
                indicators["international_trade"] = True
        
        # Add state-specific indicators
        if states:
            state = states[0]
            if state == "CA":
                indicators["high_gdp"] = True
                indicators["tech_industry"] = True
            elif state == "NY":
                indicators["financial_services"] = True
                indicators["high_gdp"] = True
            elif state == "TX":
                indicators["energy_sector"] = True
                indicators["business_friendly"] = True
        
        return indicators
    
    def _get_demographic_indicators(self, primary_region: Optional[str], states: List[str]) -> Dict[str, Any]:
        """Get demographic indicators for the region."""
        indicators = {}
        
        if primary_region:
            if "New York" in primary_region or "Los Angeles" in primary_region:
                indicators["diverse_population"] = True
                indicators["young_professionals"] = True
                indicators["international_community"] = True
            elif "San Francisco" in primary_region:
                indicators["tech_workers"] = True
                indicators["high_education"] = True
                indicators["young_professionals"] = True
            elif "Miami" in primary_region:
                indicators["hispanic_population"] = True
                indicators["international_community"] = True
        
        return indicators
    
    def _analyze_geographic_features(self, regions: List[str], states: List[str]) -> List[str]:
        """Analyze geographic features of the regions."""
        features = []
        
        # Analyze based on regions
        for region in regions:
            if "New York" in region:
                features.extend(["coastal", "harbor", "rivers"])
            elif "Los Angeles" in region:
                features.extend(["coastal", "mountains", "desert_proximity"])
            elif "San Francisco" in region:
                features.extend(["coastal", "bay", "hills"])
            elif "Chicago" in region:
                features.extend(["lakefront", "flat_terrain"])
            elif "Miami" in region:
                features.extend(["coastal", "tropical", "beaches"])
            elif "Phoenix" in region:
                features.extend(["desert", "mountains", "dry_climate"])
            elif "Seattle" in region:
                features.extend(["coastal", "mountains", "forests"])
            elif "Boston" in region:
                features.extend(["coastal", "historic", "harbor"])
        
        # Analyze based on states
        for state in states:
            if state == "CA":
                features.extend(["pacific_coast", "diverse_geography"])
            elif state == "NY":
                features.extend(["atlantic_coast", "great_lakes"])
            elif state == "TX":
                features.extend(["gulf_coast", "plains", "desert"])
            elif state == "FL":
                features.extend(["gulf_coast", "atlantic_coast", "tropical"])
            elif state == "AZ":
                features.extend(["desert", "grand_canyon", "mountains"])
            elif state == "WA":
                features.extend(["pacific_coast", "mountains", "rainforest"])
        
        return list(set(features))  # Remove duplicates
    
    def _analyze_market_characteristics(self, regions: List[str], region_type: Optional[RegionType]) -> List[str]:
        """Analyze market characteristics based on regions."""
        characteristics = []
        
        if region_type == RegionType.URBAN:
            characteristics.extend([
                "high_population_density",
                "diverse_demographics",
                "competitive_market",
                "high_disposable_income",
                "technology_adoption"
            ])
        elif region_type == RegionType.SUBURBAN:
            characteristics.extend([
                "family_oriented",
                "moderate_population_density",
                "stable_market",
                "middle_income",
                "traditional_values"
            ])
        elif region_type == RegionType.RURAL:
            characteristics.extend([
                "low_population_density",
                "close_community",
                "price_sensitive",
                "traditional_markets",
                "local_focus"
            ])
        
        # Add region-specific characteristics
        for region in regions:
            if "New York" in region:
                characteristics.extend(["fast_paced", "high_end_consumption", "global_market"])
            elif "Los Angeles" in region:
                characteristics.extend(["creative_industry", "entertainment_focus", "diverse_culture"])
            elif "San Francisco" in region:
                characteristics.extend(["tech_savvy", "innovation_focused", "sustainability_minded"])
            elif "Chicago" in region:
                characteristics.extend(["business_hub", "manufacturing", "logistics_center"])
        
        return list(set(characteristics))
