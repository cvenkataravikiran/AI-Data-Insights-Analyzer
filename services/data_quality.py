"""
Data Quality Assessment Module
Comprehensive data quality analysis and scoring
"""

import pandas as pd
import numpy as np

class DataQualityAssessor:
    def __init__(self, df):
        self.df = df.copy()
    
    def assess_quality(self):
        """Comprehensive data quality assessment"""
        report = {
            'overall_score': 0,
            'dimensions': {},
            'missing_summary': pd.DataFrame(),
            'duplicate_count': 0,
            'complete_rows': 0,
            'valid_percentage': 0,
            'column_quality': pd.DataFrame(),
            'recommendations': []
        }
        
        # Calculate quality dimensions
        completeness = self._calculate_completeness()
        consistency = self._calculate_consistency()
        uniqueness = self._calculate_uniqueness()
        validity = self._calculate_validity()
        
        report['dimensions'] = {
            'completeness': completeness,
            'consistency': consistency,
            'uniqueness': uniqueness,
            'validity': validity
        }
        
        # Overall score (weighted average)
        report['overall_score'] = (
            completeness * 0.3 +
            consistency * 0.25 +
            uniqueness * 0.2 +
            validity * 0.25
        )
        
        # Missing value analysis
        report['missing_summary'] = self._get_missing_summary()
        
        # Duplicate analysis
        report['duplicate_count'] = self.df.duplicated().sum()
        
        # Complete rows
        report['complete_rows'] = len(self.df.dropna())
        report['valid_percentage'] = (report['complete_rows'] / len(self.df)) * 100
        
        # Column-wise quality
        report['column_quality'] = self._get_column_quality()
        
        # Generate recommendations
        report['recommendations'] = self._generate_recommendations(report)
        
        return report
    
    def _calculate_completeness(self):
        """Calculate completeness score (non-null values)"""
        total_cells = self.df.shape[0] * self.df.shape[1]
        if total_cells == 0:
            return 100.0
        
        non_null_cells = self.df.count().sum()
        completeness = (non_null_cells / total_cells) * 100
        
        return completeness
    
    def _calculate_consistency(self):
        """Calculate consistency score (data type consistency)"""
        consistency_scores = []
        
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                # For text columns, check format consistency
                non_null = self.df[col].dropna()
                if len(non_null) == 0:
                    consistency_scores.append(100)
                    continue
                
                # Check if values follow similar patterns
                lengths = non_null.astype(str).str.len()
                std_dev = lengths.std()
                mean_len = lengths.mean()
                
                if mean_len == 0:
                    consistency_scores.append(100)
                else:
                    cv = (std_dev / mean_len) * 100  # Coefficient of variation
                    # Lower CV means more consistent
                    score = max(0, 100 - min(cv, 100))
                    consistency_scores.append(score)
            
            elif pd.api.types.is_numeric_dtype(self.df[col]):
                # For numeric columns, check for outliers
                non_null = self.df[col].dropna()
                if len(non_null) == 0:
                    consistency_scores.append(100)
                    continue
                
                Q1 = non_null.quantile(0.25)
                Q3 = non_null.quantile(0.75)
                IQR = Q3 - Q1
                
                if IQR == 0:
                    consistency_scores.append(100)
                    continue
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = ((non_null < lower_bound) | (non_null > upper_bound)).sum()
                outlier_pct = (outliers / len(non_null)) * 100
                
                # Fewer outliers = higher consistency
                score = max(0, 100 - (outlier_pct * 2))
                consistency_scores.append(score)
            else:
                consistency_scores.append(100)
        
        return np.mean(consistency_scores) if consistency_scores else 100.0
    
    def _calculate_uniqueness(self):
        """Calculate uniqueness score (non-duplicate records)"""
        total_rows = len(self.df)
        if total_rows == 0:
            return 100.0
        
        duplicate_rows = self.df.duplicated().sum()
        uniqueness = ((total_rows - duplicate_rows) / total_rows) * 100
        
        return uniqueness
    
    def _calculate_validity(self):
        """Calculate validity score (valid data types and ranges)"""
        validity_scores = []
        
        for col in self.df.columns:
            non_null = self.df[col].dropna()
            if len(non_null) == 0:
                validity_scores.append(100)
                continue
            
            # Check for negative values in potentially positive-only columns
            col_lower = col.lower()
            if pd.api.types.is_numeric_dtype(self.df[col]):
                if any(keyword in col_lower for keyword in ['quantity', 'count', 'age', 'price', 'sales', 'revenue']):
                    negative_count = (non_null < 0).sum()
                    negative_pct = (negative_count / len(non_null)) * 100
                    score = max(0, 100 - (negative_pct * 5))
                    validity_scores.append(score)
                else:
                    validity_scores.append(100)
            else:
                # For text fields, check for empty strings
                empty_count = (non_null.astype(str).str.strip() == '').sum()
                empty_pct = (empty_count / len(non_null)) * 100
                score = max(0, 100 - (empty_pct * 2))
                validity_scores.append(score)
        
        return np.mean(validity_scores) if validity_scores else 100.0
    
    def _get_missing_summary(self):
        """Get missing value summary"""
        missing_data = self.df.isnull().sum()
        missing_percent = (missing_data / len(self.df)) * 100
        
        summary = pd.DataFrame({
            'Column': missing_data.index,
            'Missing Count': missing_data.values,
            'Percentage': missing_percent.values.round(2)
        })
        
        summary = summary[summary['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        return summary
    
    def _get_column_quality(self):
        """Get column-wise quality metrics"""
        col_metrics = []
        
        for col in self.df.columns:
            completeness = (self.df[col].count() / len(self.df)) * 100
            unique_pct = (self.df[col].nunique() / len(self.df)) * 100 if len(self.df) > 0 else 0
            
            col_metrics.append({
                'Column': col,
                'Type': str(self.df[col].dtype),
                'Completeness %': round(completeness, 2),
                'Unique Values': self.df[col].nunique(),
                'Uniqueness %': round(unique_pct, 2)
            })
        
        return pd.DataFrame(col_metrics)
    
    def _generate_recommendations(self, report):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Check completeness
        if report['dimensions']['completeness'] < 80:
            recommendations.append(
                "Data completeness is below 80%. Consider handling missing values through imputation or removal."
            )
        
        # Check duplicates
        if report['duplicate_count'] > 0:
            dup_pct = (report['duplicate_count'] / len(self.df)) * 100
            recommendations.append(
                f"Found {report['duplicate_count']} duplicate rows ({dup_pct:.1f}%). Review and remove duplicates to improve data quality."
            )
        
        # Check consistency
        if report['dimensions']['consistency'] < 70:
            recommendations.append(
                "Data consistency is low. Review column formats and standardize data entry patterns."
            )
        
        # Check validity
        if report['dimensions']['validity'] < 80:
            recommendations.append(
                "Some data values may be invalid. Review numeric ranges and text formats for accuracy."
            )
        
        # Check uniqueness
        if report['dimensions']['uniqueness'] < 90:
            recommendations.append(
                "High duplicate rate detected. Ensure each record represents a unique transaction or entity."
            )
        
        # Column-specific recommendations
        missing_summary = report['missing_summary']
        if not missing_summary.empty:
            high_missing = missing_summary[missing_summary['Percentage'] > 30]
            if not high_missing.empty:
                cols = ', '.join(high_missing['Column'].tolist()[:3])
                recommendations.append(
                    f"Columns with >30% missing data: {cols}. Consider dropping these columns or investigating data collection issues."
                )
        
        return recommendations if recommendations else ["Data quality is excellent! No immediate actions required."]
