"""Excel Invoice Parser - Fixed Version"""

import pandas as pd
from typing import Dict

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
            
            # Convert to DataFrame if it's not already
            if not isinstance(df, pd.DataFrame):
                return {
                    "success": False,
                    "error": "Invalid Excel format"
                }
            
            # Check if DataFrame is empty
            if df.empty:
                return {
                    "success": False,
                    "error": "Excel file is empty"
                }
            
            # Check if all required columns exist
            missing_cols = [col for col in self.required_columns 
                          if col not in df.columns]
            
            if missing_cols:
                return {
                    "success": False,
                    "error": f"Missing columns: {', '.join(missing_cols)}"
                }
            
            # Extract header information (from first row)
            # Use .iloc[0] safely with error handling
            try:
                invoice_number = str(df['Invoice Number'].iloc[0]) if not df['Invoice Number'].empty else "N/A"
                invoice_date = str(df['Invoice Date'].iloc[0]) if not df['Invoice Date'].empty else "N/A"
                gstin_seller = str(df['GSTIN Seller'].iloc[0]) if not df['GSTIN Seller'].empty else "N/A"
                gstin_buyer = str(df['GSTIN Buyer'].iloc[0]) if not df['GSTIN Buyer'].empty else "N/A"
                
                # Handle Place of Supply (optional column)
                if 'Place of Supply' in df.columns:
                    place_of_supply = str(df['Place of Supply'].iloc[0])
                else:
                    place_of_supply = '27'  # Default
                
            except (IndexError, KeyError) as e:
                return {
                    "success": False,
                    "error": f"Error reading header data: {str(e)}"
                }
            
            invoice_data = {
                "invoice_number": invoice_number,
                "invoice_date": invoice_date,
                "gstin_seller": gstin_seller,
                "gstin_buyer": gstin_buyer,
                "place_of_supply": place_of_supply,
                "items": []
            }
            
            # Extract items (iterate through all rows)
            for idx, row in df.iterrows():
                try:
                    # Skip rows with missing critical data
                    if pd.isna(row['Item Name']) or pd.isna(row['HSN Code']):
                        continue
                    
                    # Parse numeric values safely
                    quantity = float(row['Quantity']) if not pd.isna(row['Quantity']) else 0
                    unit_price = float(row['Unit Price']) if not pd.isna(row['Unit Price']) else 0
                    gst_rate = float(row['GST Rate']) if not pd.isna(row['GST Rate']) else 0
                    
                    taxable_value = quantity * unit_price
                    
                    item = {
                        "item_number": idx + 1,
                        "item_name": str(row['Item Name']),
                        "hsn_code": str(row['HSN Code']),
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "gst_rate": gst_rate,
                        "taxable_value": round(taxable_value, 2)
                    }
                    
                    # Calculate GST
                    gst_amount = taxable_value * (gst_rate / 100)
                    item['gst_amount'] = round(gst_amount, 2)
                    item['total_amount'] = round(taxable_value + gst_amount, 2)
                    
                    invoice_data["items"].append(item)
                    
                except Exception as e:
                    # Skip problematic rows but continue processing
                    continue
            
            # Check if we got any items
            if not invoice_data["items"]:
                return {
                    "success": False,
                    "error": "No valid items found in invoice"
                }
            
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