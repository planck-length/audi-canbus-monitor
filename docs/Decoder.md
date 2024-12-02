# Audi CAN Bus Data Decoder and Monitoring

This component of the Audi CAN Bus Logger project focuses on decoding and storing CAN bus data using Python, cantools, and InfluxDB. It leverages the `can` library to receive messages from a SocketCAN interface (or a virtual CAN interface for testing) and `cantools` to decode these messages based on a DBC file. The decoded data is then stored in InfluxDB for visualization and analysis.

## Features

* **Real-time Decoding:** Decodes CAN bus messages in real-time using a provided DBC file (`vw_mqb_2010.dbc` in this example).
* **InfluxDB Integration:** Stores both raw and decoded CAN data in InfluxDB, allowing for time-series analysis and visualization.
* **SocketCAN Support:** Listens for CAN messages on a specified SocketCAN interface.  Defaults to `vcan0` but can be overridden via command-line argument.
* **Dockerized Deployment:**  Uses Docker Compose for easy deployment and management of InfluxDB and Grafana.

## Requirements

* Python 3
* Required Python packages (install via `pip install -r requirements.txt`):
    * `can`
    * `cantools`
    * `influxdb-client`
* Docker and Docker Compose (for running InfluxDB and Grafana)
* A DBC file describing the CAN messages (e.g., `vw_mqb_2010.dbc`)
* [Optional] A real or virtual CAN interface (e.g., `vcan0`)

## Setup and Usage

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd audi-can-logger
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install -r python/requirements.txt
   ```

3. **Configure InfluxDB Connection:**
   - Copy the `influxdb2/influx-configs.example` file to `influxdb2/influx-configs` and fill in the correct values for your InfluxDB instance (token, org).  This avoids hardcoding credentials in the Python script.
   - The `docker-compose.yaml` file sets up InfluxDB with default credentials (admin/admin12345678), a new organization (`vimac`), and a bucket called `can_monitoring`.


4. **Start InfluxDB and Grafana (using Docker Compose):**
   ```bash
   docker-compose up -d
   ```
   This will start InfluxDB and Grafana containers in the background.  Grafana will be accessible at `http://localhost:3000` with credentials `admin:admin`.


5. **[Optional] Set up a Virtual CAN Interface (for testing):**
   ```bash
   sudo modprobe vcan
   sudo ip link add dev vcan0 type vcan
   sudo ip link set up vcan0
   ```

6. **Run the Python Script:**
   ```bash
   python python/can_analyze.py <SOCKET>
   ```
   Replace `<SOCKET>` with the name of your CAN interface (e.g., `can0`, `vcan0`).  If omitted, it defaults to `vcan0`.

7. **Send CAN Messages:**
   Use a CAN bus tool (like `cansend`) to send messages on the specified interface.  The script will decode and store them in InfluxDB. If using `vcan0`, you can use `cansend vcan0 <arbitration_id>#<data>`


8. **Visualize Data in Grafana:**
   - Access Grafana at `http://localhost:3000` and log in.
   - Add InfluxDB as a data source, pointing to `http://influxdb2:8086`. Use the credentials defined in your `influxdb2/influx-configs` file.
   - Create dashboards to visualize the stored CAN data.

## Code Overview (`can_analyze.py`)

* **Imports:** Imports necessary libraries (`can`, `cantools`, `influxdb_client`, etc.).
* **DBC Loading:** Loads the DBC file (`vw_mqb_2010.dbc`) for message decoding.
* **InfluxDB Connection:**  Connects to the InfluxDB instance using parameters loaded from the configuration file.
* **CAN Message Reception:** Continuously receives CAN messages from the specified SocketCAN interface.
* **Decoding and Storage:** Decodes received messages using the DBC file and stores both raw (hexadecimal data) and decoded values in InfluxDB.
* **Error Handling:** Includes basic error handling for database lookup failures and decoding errors.

## Docker Compose (`docker-compose.yaml`)

The `docker-compose.yaml` file defines the services for InfluxDB and Grafana:

* **`influxdb2`:** Sets up the InfluxDB service with persistent storage and initializes a default organization, bucket, and user.
* **`grafana`:** Sets up the Grafana service with persistent storage.
* **Networking:** Creates a bridge network for communication between the containers.

This improved documentation provides clearer instructions for setup, usage, and code understanding, making it easier to run and adapt the CAN data decoding and monitoring component. Remember to replace placeholders like `<repository_url>` and `<SOCKET>` with actual values.