"""GST Invoice Validator"""

import re
from typing import Dict, List
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.gst_rules import GST_RULES, get_gst_rate, get_mandatory_fields

class GSTValidator:
    """Validate invoices against GST rules"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate(self, invoice_data: Dict) -> Dict:
        """
        Validate invoice data
        
        Args:
            invoice_data: Parsed invoice data
            
        Returns:
            Validation results with errors and warnings
        """
        self.errors = []
        self.warnings = []
        
        # Validate mandatory fields
        self._validate_mandatory_fields(invoice_data)
        
        # Validate GSTIN format
        self._validate_gstin(invoice_data.get('gstin_seller'), 'Seller')
        self._validate_gstin(invoice_data.get('gstin_buyer'), 'Buyer')
        
        # Validate items
        for item in invoice_data.get('items', []):
            self._validate_item(item)
        
        return {
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    def _validate_mandatory_fields(self, invoice_data: Dict):
        """Check if all mandatory fields are present"""
        mandatory = get_mandatory_fields()
        
        for field in mandatory:
            if field not in invoice_data or not invoice_data[field]:
                self.errors.append({
                    "field": field,
                    "error_type": "missing_field",
                    "message": f"{field} is mandatory",
                    "severity": "high"
                })
    
    def _validate_gstin(self, gstin: str, party: str):
        """Validate GSTIN format"""
        if not gstin:
            return
        
        # Check length
        if len(gstin) != 15:
            self.errors.append({
                "field": f"gstin_{party.lower()}",
                "error_type": "invalid_format",
                "message": f"{party} GSTIN must be 15 characters",
                "current_value": gstin,
                "severity": "high"
            })
            return
        
        # Check pattern
        pattern = GST_RULES["gstin_format"]["pattern"]
        if not re.match(pattern, gstin):
            self.errors.append({
                "field": f"gstin_{party.lower()}",
                "error_type": "invalid_format",
                "message": f"{party} GSTIN format is invalid",
                "current_value": gstin,
                "severity": "high"
            })
    
    def _validate_item(self, item: Dict):
        """Validate individual item"""
        hsn_code = str(item.get('hsn_code', ''))
        gst_rate = item.get('gst_rate', 0)
        
        # Validate HSN format
        if not re.match(r'^\d{4}$|^\d{8}$', hsn_code):
            self.errors.append({
                "field": f"items[{item['item_number']}].hsn_code",
                "error_type": "invalid_format",
                "message": f"HSN code must be 4 or 8 digits",
                "current_value": hsn_code,
                "severity": "high"
            })
            return
        
        # Validate GST rate for known HSN codes
        correct_rate = get_gst_rate(hsn_code)
        
        if correct_rate is not None and correct_rate != gst_rate:
            self.errors.append({
                "field": f"items[{item['item_number']}].gst_rate",
                "error_type": "incorrect_gst_rate",
                "message": f"Wrong GST rate for HSN {hsn_code}",
                "current_value": gst_rate,
                "expected_value": correct_rate,
                "severity": "high"
            })
        elif correct_rate is None:
            self.warnings.append({
                "field": f"items[{item['item_number']}].hsn_code",
                "message": f"HSN code {hsn_code} not in database. Please verify manually.",
                "severity": "low"
            })
