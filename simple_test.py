import unittest
import pandas as pd
import sys
import os

# Add the current directory to the path so we can import our app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import load_data, create_figure

class TestCoreFunctionality(unittest.TestCase):
    """Test core functionality of the Soul Foods application"""
    
    def test_data_loading(self):
        """Test that data loads correctly"""
        print("Testing data loading...")
        df = load_data()
        
        # Basic checks
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        print(f"✅ Data loaded successfully: {len(df)} records")
        
        # Column checks
        required_columns = ['sales', 'date', 'region']
        for col in required_columns:
            self.assertIn(col, df.columns)
        print(f"✅ All required columns present: {required_columns}")
        
        # Data type checks
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['date']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['sales']))
        print("✅ Data types are correct")
    
    def test_region_filtering(self):
        """Test region filtering functionality"""
        print("Testing region filtering...")
        df = load_data()
        
        regions = ['north', 'south', 'east', 'west']
        for region in regions:
            filtered_df = df[df['region'] == region]
            self.assertGreater(len(filtered_df), 0)
            print(f"✅ {region.title()} region: {len(filtered_df)} records")
    
    def test_figure_creation(self):
        """Test that figures can be created for all regions"""
        print("Testing figure creation...")
        
        regions = ['all', 'north', 'south', 'east', 'west']
        for region in regions:
            try:
                fig = create_figure(region)
                self.assertIsNotNone(fig)
                print(f"✅ Figure created for {region} region")
            except Exception as e:
                self.fail(f"Failed to create figure for {region}: {e}")
    
    def test_sales_analysis(self):
        """Test sales analysis calculations"""
        print("Testing sales analysis...")
        df = load_data()
        
        # Test price change date analysis
        price_change_date = pd.to_datetime('2021-01-15')
        before_data = df[df['date'] < price_change_date]
        after_data = df[df['date'] >= price_change_date]
        
        self.assertGreater(len(before_data), 0)
        self.assertGreater(len(after_data), 0)
        
        before_avg = before_data['sales'].mean()
        after_avg = after_data['sales'].mean()
        
        print(f"✅ Before price increase: ${before_avg:,.0f} average daily sales")
        print(f"✅ After price increase: ${after_avg:,.0f} average daily sales")
        
        # Calculate percentage change
        change_pct = ((after_avg - before_avg) / before_avg) * 100
        print(f"✅ Sales change: {change_pct:+.1f}%")
        
        # Verify the expected result (sales should be higher after price increase)
        self.assertGreater(after_avg, before_avg)
        print("✅ Sales increased after price increase (as expected)")
    
    def test_data_integrity(self):
        """Test data integrity and reasonableness"""
        print("Testing data integrity...")
        df = load_data()
        
        # Check for missing values
        missing_sales = df['sales'].isnull().sum()
        missing_dates = df['date'].isnull().sum()
        missing_regions = df['region'].isnull().sum()
        
        self.assertEqual(missing_sales, 0)
        self.assertEqual(missing_dates, 0)
        self.assertEqual(missing_regions, 0)
        print("✅ No missing values found")
        
        # Check sales are positive
        negative_sales = (df['sales'] <= 0).sum()
        self.assertEqual(negative_sales, 0)
        print("✅ All sales values are positive")
        
        # Check date range
        min_date = df['date'].min()
        max_date = df['date'].max()
        print(f"✅ Date range: {min_date.date()} to {max_date.date()}")
        
        # Check regions
        unique_regions = df['region'].unique()
        expected_regions = ['north', 'south', 'east', 'west']
        self.assertEqual(set(unique_regions), set(expected_regions))
        print(f"✅ All expected regions present: {list(unique_regions)}")

def run_simple_tests():
    """Run the simple test suite"""
    print("🧪 Running Simple Test Suite for Soul Foods Application")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    tests = unittest.TestLoader().loadTestsFromTestCase(TestCoreFunctionality)
    test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        print("🎉 All tests passed! The application is working correctly.")
        print(f"📊 Tests run: {result.testsRun}")
        print(f"✅ Failures: {len(result.failures)}")
        print(f"⚠️  Errors: {len(result.errors)}")
        return True
    else:
        print("❌ Some tests failed. Please review the output above.")
        print(f"📊 Tests run: {result.testsRun}")
        print(f"🎯 Failures: {len(result.failures)}")
        print(f"🚨 Errors: {len(result.errors)}")
        return False

if __name__ == '__main__':
    success = run_simple_tests()
    exit(0 if success else 1) 