# Ruuvi Collector

This is a Flask app that collects data from Ruuvi Station devices and writes it to an InfluxDB database. It can be deployed on an Apache web server or any alternative web server.

## Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/RuuviCollector.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure the Flask app:

    - Open the `config.py` file and update the database connection details.
    
    - Set the following environment variables in your system or in a `.env` file:
    
        - `INFLUXDB_HOST`: The hostname or IP address of your InfluxDB server.
        - `INFLUXDB_PORT`: The port number of your InfluxDB server.
        - `INFLUXDB_USERNAME`: The username for accessing your InfluxDB server.
        - `INFLUXDB_PASSWORD`: The password for accessing your InfluxDB server.
        - `INFLUXDB_DATABASE`: The name of the InfluxDB database to write data to.

4. Deploy the app on your web server:

    - If using Apache, create a new virtual host configuration file and add the following:

      ```apache
      <VirtualHost *:80>
            ServerName your-domain.com
            DocumentRoot /path/to/RuuviCollector

            WSGIDaemonProcess ruuvi-collector user=your-username group=your-group threads=5
            WSGIScriptAlias / /path/to/RuuviCollector/wsgi.py

            <Directory /path/to/RuuviCollector>
                 WSGIProcessGroup ruuvi-collector
                 WSGIApplicationGroup %{GLOBAL}
                 Require all granted
            </Directory>
      </VirtualHost>
      ```

    - If using an alternative web server, refer to its documentation for deployment instructions.

5. Configure Ruuvi Station proxy server settings:

    - Open the Ruuvi Station app and go to the settings.
    - Find the "Proxy Server" option and enter the URL of your deployed app.
    - Save the settings.

## Usage

Once the app is deployed and the Ruuvi Station proxy server settings are configured, the app will start collecting data from Ruuvi Station devices and writing it to the InfluxDB database.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.