# Ad Pricing Optimization

This project uses LSTM models for dynamic ad pricing to optimize ad revenue. It includes a Dash dashboard for visualizing the results.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/ad-pricing-optimization.git
   cd ad-pricing-optimization
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the Dash app:
   ```
   python app/main.py
   ```

## Project Structure

- `data/`: Contains the dataset used for training and testing.
- `models/`: Includes the LSTM model implementation.
- `utils/`: Contains utility functions for data preprocessing and evaluation.
- `app/`: Dash application for the dashboard.
- `tests/`: Unit tests for the project components.

## Usage

1. Prepare your data and place it in the `data/` directory.
2. Run the Jupyter notebook in the `notebooks/` directory for exploratory data analysis.
3. Train the LSTM model using the `models/lstm_model.py` script.
4. Launch the Dash app to visualize the results and optimize ad pricing.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
