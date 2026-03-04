"""Excel Invoice Parser - Fixed for Percentage Format"""

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
    
    def _parse_percentage(self, value):
        """Convert percentage string to number (e.g., '18%' -> 18)"""
        if pd.isna(value):
            return 0
        
        # Convert to string and remove % symbol
        str_value = str(value).strip().replace('%', '')
        
        try:
            return float(str_value)
        except:
            return 0
    
    def _parse_number(self, value):
        """Safely parse numeric values"""
        if pd.isna(value):
            return 0
        try:
            return float(value)
        except:
            return 0
    
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
            try:
                invoice_number = str(df['Invoice Number'].iloc[0]) if not df['Invoice Number'].empty else "N/A"
                invoice_date = str(df['Invoice Date'].iloc[0]) if not df['Invoice Date'].empty else "N/A"
                gstin_seller = str(df['GSTIN Seller'].iloc[0]) if not df['GSTIN Seller'].empty else "N/A"
                gstin_buyer = str(df['GSTIN Buyer'].iloc[0]) if not df['GSTIN Buyer'].empty else "N/A"
                
                # Handle Place of Supply (optional column)
                if 'Place of Supply' in df.columns:
                    place_of_supply = str(df['Place of Supply'].iloc[0])
                else:
                    # Extract from GSTIN (first 2 digits)
                    place_of_supply = gstin_seller[:2] if len(gstin_seller) >= 2 else '27'
                
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
                    
                    # Parse numeric values safely - HANDLE PERCENTAGE!
                    quantity = self._parse_number(row['Quantity'])
                    unit_price = self._parse_number(row['Unit Price'])
                    gst_rate = self._parse_percentage(row['GST Rate'])  # ✅ Handles "18%"
                    
                    # Skip if quantity or price is 0
                    if quantity <= 0 or unit_price <= 0:
                        continue
                    
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
                    print(f"Warning: Skipped row {idx + 1}: {str(e)}")
                    continue
            
            # Check if we got any items
            if not invoice_data["items"]:
                return {
                    "success": False,
                    "error": "No valid items found in invoice. Please check that Item Name, HSN Code, Quantity, Unit Price, and GST Rate are filled correctly."
                }
            
            # Calculate totals
            invoice_data["total_taxable_value"] = round(sum(
                item['taxable_value'] for item in invoice_data["items"]
            ), 2)
            invoice_data["total_gst"] = round(sum(
                item['gst_amount'] for item in invoice_data["items"]
            ), 2)
            invoice_data["total_amount"] = round(sum(
                item['total_amount'] for item in invoice_data["items"]
            ), 2)
            
            return {
                "success": True,
                "data": invoice_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error parsing file: {str(e)}"
            }