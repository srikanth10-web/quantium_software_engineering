import unittest
import pandas as pd
import plotly.graph_objects as go
from dash.testing.application_runners import import_app
from dash.testing.composite import DashComposite
from dash.testing.browser import Browser
import sys
import os

# Add the current directory to the path so we can import our app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import load_data, create_figure

class TestDataProcessing(unittest.TestCase):
    """Test data processing functions"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = pd.DataFrame({
            'sales': [1500, 1600, 1700, 1800, 1900],
            'date': pd.to_datetime(['2018-02-06', '2018-02-07', '2018-02-08', '2018-02-09', '2018-02-10']),
            'region': ['north', 'south', 'east', 'west', 'north']
        })
    
    def test_load_data(self):
        """Test that load_data function loads and processes data correctly"""
        df = load_data()
        
        # Check that data is loaded
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
        
        # Check required columns exist
        required_columns = ['sales', 'date', 'region']
        for col in required_columns:
            self.assertIn(col, df.columns)
        
        # Check data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['date']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['sales']))
        self.assertTrue(pd.api.types.is_object_dtype(df['region']))
        
        # Check regions
        expected_regions = ['north', 'south', 'east', 'west']
        for region in df['region'].unique():
            self.assertIn(region, expected_regions)
    
    def test_create_figure_all_regions(self):
        """Test create_figure function with 'all' regions"""
        fig = create_figure('all')
        
        # Check that figure is created
        self.assertIsInstance(fig, go.Figure)
        
        # Check subplot structure
        self.assertEqual(len(fig.data), 2)  # Sales line and price line
        
        # Check that data exists
        self.assertGreater(len(fig.data[0].x), 0)
        self.assertGreater(len(fig.data[0].y), 0)
    
    def test_create_figure_specific_region(self):
        """Test create_figure function with specific region"""
        regions = ['north', 'south', 'east', 'west']
        
        for region in regions:
            fig = create_figure(region)
            
            # Check that figure is created
            self.assertIsInstance(fig, go.Figure)
            
            # Check subplot titles contain region name
            self.assertIn(region.title(), fig.layout.title.text)
    
    def test_create_figure_empty_data(self):
        """Test create_figure function handles empty data gracefully"""
        # This should not raise an exception
        fig = create_figure('nonexistent_region')
        self.assertIsInstance(fig, go.Figure)

class TestDataValidation(unittest.TestCase):
    """Test data validation and integrity"""
    
    def test_sales_data_integrity(self):
        """Test that sales data is reasonable"""
        df = load_data()
        
        # Check sales are positive
        self.assertTrue((df['sales'] > 0).all())
        
        # Check sales are within reasonable range (based on our known data)
        self.assertTrue((df['sales'] < 10000).all())  # Should be less than $10k per day
        
        # Check no missing values
        self.assertFalse(df['sales'].isnull().any())
        self.assertFalse(df['date'].isnull().any())
        self.assertFalse(df['region'].isnull().any())
    
    def test_date_range(self):
        """Test that dates are within expected range"""
        df = load_data()
        
        # Check date range (should be 2018-2022 based on our data)
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        self.assertGreaterEqual(min_date, pd.to_datetime('2018-01-01'))
        self.assertLessEqual(max_date, pd.to_datetime('2022-12-31'))
    
    def test_region_distribution(self):
        """Test that all regions have data"""
        df = load_data()
        
        regions = df['region'].value_counts()
        
        # Check all four regions have data
        self.assertEqual(len(regions), 4)
        
        # Check regions are roughly balanced (within 20% of each other)
        min_count = regions.min()
        max_count = regions.max()
        balance_ratio = min_count / max_count
        self.assertGreater(balance_ratio, 0.8)

class TestPriceChangeAnalysis(unittest.TestCase):
    """Test price change analysis logic"""
    
    def test_price_change_date_identification(self):
        """Test that price change date is correctly identified"""
        df = load_data()
        
        # Price change should be on 2021-01-15
        price_change_date = pd.to_datetime('2021-01-15')
        
        # Check that we have data before and after this date
        before_data = df[df['date'] < price_change_date]
        after_data = df[df['date'] >= price_change_date]
        
        self.assertGreater(len(before_data), 0)
        self.assertGreater(len(after_data), 0)
    
    def test_sales_comparison_logic(self):
        """Test sales comparison before and after price change"""
        df = load_data()
        price_change_date = pd.to_datetime('2021-01-15')
        
        # Calculate averages
        before_avg = df[df['date'] < price_change_date]['sales'].mean()
        after_avg = df[df['date'] >= price_change_date]['sales'].mean()
        
        # Check that averages are reasonable
        self.assertGreater(before_avg, 0)
        self.assertGreater(after_avg, 0)
        
        # Check that we can calculate percentage change
        if before_avg > 0:
            change_pct = ((after_avg - before_avg) / before_avg) * 100
            self.assertIsInstance(change_pct, float)

class TestRegionalAnalysis(unittest.TestCase):
    """Test regional analysis functionality"""
    
    def test_region_filtering(self):
        """Test that region filtering works correctly"""
        df = load_data()
        
        regions = ['north', 'south', 'east', 'west']
        
        for region in regions:
            filtered_df = df[df['region'] == region]
            
            # Check that filtering works
            self.assertTrue((filtered_df['region'] == region).all())
            
            # Check that we have data for each region
            self.assertGreater(len(filtered_df), 0)
    
    def test_regional_sales_comparison(self):
        """Test regional sales comparison"""
        df = load_data()
        
        regions = ['north', 'south', 'east', 'west']
        regional_averages = {}
        
        for region in regions:
            regional_df = df[df['region'] == region]
            regional_averages[region] = regional_df['sales'].mean()
        
        # Check that all regions have reasonable sales averages
        for region, avg in regional_averages.items():
            self.assertGreater(avg, 0)
            self.assertLess(avg, 10000)  # Should be reasonable daily sales

class TestFigureProperties(unittest.TestCase):
    """Test figure properties and layout"""
    
    def test_figure_layout_properties(self):
        """Test that figures have correct layout properties"""
        fig = create_figure('all')
        
        # Check layout properties
        self.assertIsNotNone(fig.layout.title)
        self.assertIsNotNone(fig.layout.xaxis)
        self.assertIsNotNone(fig.layout.yaxis)
        
        # Check subplot structure
        self.assertEqual(len(fig.data), 2)  # Sales and price lines
    
    def test_figure_interactivity(self):
        """Test that figures have interactive properties"""
        fig = create_figure('all')
        
        # Check hover template exists
        self.assertIsNotNone(fig.data[0].hovertemplate)
        self.assertIsNotNone(fig.data[1].hovertemplate)
        
        # Check hover mode is set
        self.assertEqual(fig.layout.hovermode, 'x unified')

class TestAppStructure(unittest.TestCase):
    """Test app structure and components"""
    
    def test_app_import(self):
        """Test that app can be imported"""
        try:
            from app import app
            self.assertIsNotNone(app)
        except ImportError as e:
            self.fail(f"Failed to import app: {e}")
    
    def test_app_layout(self):
        """Test that app has a layout"""
        from app import app
        self.assertIsNotNone(app.layout)

def run_tests():
    """Run all tests and return results"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataProcessing,
        TestDataValidation,
        TestPriceChangeAnalysis,
        TestRegionalAnalysis,
        TestFigureProperties,
        TestAppStructure
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == '__main__':
    print("🧪 Running comprehensive test suite for Soul Foods Dash Application...")
    print("=" * 70)
    
    result = run_tests()
    
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ All tests passed! The application is working correctly.")
        print(f"📊 Tests run: {result.testsRun}")
        print(f"🎯 Failures: {len(result.failures)}")
        print(f"⚠️  Errors: {len(result.errors)}")
    else:
        print("❌ Some tests failed. Please review the output above.")
        print(f"📊 Tests run: {result.testsRun}")
        print(f"🎯 Failures: {len(result.failures)}")
        print(f"⚠️  Errors: {len(result.errors)}")
        
        if result.failures:
            print("\n🔍 Failures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\n🚨 Errors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}") 