"""Excel Invoice Parser"""

import pandas as pd
from typing import Dict, List, Optional

class ExcelInvoiceParser:
    """Parse Excel invoices into structured format"""
    
    def __init__(self):
        self.required_columns = [
            'Invoice Number', 'Invoice Date', 'GSTIN Seller', 
            'GSTIN Buyer', 'Item Name', 'HSN Code', 
            'Quantity', 'Unit Price', 'GST Rate'
        ]
    
    def parse(self, file_path: str) -> Dict:
        """
        Parse Excel file and extract invoice data
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Dictionary with invoice data
        """
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Check if all required columns exist
            missing_cols = [col for col in self.required_columns 
                          if col not in df.columns]
            
            if missing_cols:
                return {
                    "success": False,
                    "error": f"Missing columns: {', '.join(missing_cols)}"
                }
            
            # Extract header information (from first row)
            invoice_data = {
                "invoice_number": str(df['Invoice Number'].iloc[0]),
                "invoice_date": str(df['Invoice Date'].iloc[0]),
                "gstin_seller": str(df['GSTIN Seller'].iloc[0]),
                "gstin_buyer": str(df['GSTIN Buyer'].iloc[0]),
                "place_of_supply": str(df.get('Place of Supply', ['27']).iloc[0]),
                "items": []
            }
            
            # Extract items
            for idx, row in df.iterrows():
                item = {
                    "item_number": idx + 1,
                    "item_name": str(row['Item Name']),
                    "hsn_code": str(row['HSN Code']),
                    "quantity": float(row['Quantity']),
                    "unit_price": float(row['Unit Price']),
                    "gst_rate": float(row['GST Rate']),
                    "taxable_value": float(row['Quantity']) * float(row['Unit Price'])
                }
                
                # Calculate GST
                gst_amount = item['taxable_value'] * (item['gst_rate'] / 100)
                item['gst_amount'] = round(gst_amount, 2)
                item['total_amount'] = round(item['taxable_value'] + gst_amount, 2)
                
                invoice_data["items"].append(item)
            
            # Calculate totals
            invoice_data["total_taxable_value"] = sum(
                item['taxable_value'] for item in invoice_data["items"]
            )
            invoice_data["total_gst"] = sum(
                item['gst_amount'] for item in invoice_data["items"]
            )
            invoice_data["total_amount"] = sum(
                item['total_amount'] for item in invoice_data["items"]
            )
            
            return {
                "success": True,
                "data": invoice_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error parsing file: {str(e)}"
            }
