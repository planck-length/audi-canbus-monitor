# Audi CAN Bus Sniffer with MCP2515 and Embassy

This embedded Rust application utilizes an STM32 microcontroller, an MCP2515 CAN controller, and the Embassy framework to sniff and transmit CAN bus messages, specifically targeting Audi vehicles. It communicates with a host computer via UART using the SLCAN protocol.

## Features

* **CAN bus sniffing:** Captures CAN bus messages from an Audi vehicle.
* **SLCAN support:**  Translates CAN messages to and from the SLCAN protocol for interaction with a computer.
* **Message forwarding:** Forwards received CAN messages to the UART interface.
* **Message injection:** Receives SLCAN formatted messages via UART and transmits them on the CAN bus.
* **Error handling:** Includes basic error handling and reporting for both CAN and UART communication.
* **User interaction:** Utilizes a button (PC13) to toggle between sniffing and injection modes.  While the button is pressed, the application will receive and forward slcan messages.

## Hardware Requirements

* STM32L476RG microcontroller (specified in Cargo.toml)
* MCP2515 CAN controller
* CAN bus transceiver
* Connections between the STM32, MCP2515, and CAN bus as follows:
    * **SPI:** STM32 (PA5/SCK, PA6/MISO, PA7/MOSI) to MCP2515 (SCK, SO, SI)
    * **CS:** STM32 (PB6) to MCP2515 (CS)
    * **INT:**  MCP2515 (INT) to a suitable STM32 pin (Not used in this example, but recommended for production)
* UART connection to a host computer (PA2/TX, PA3/RX)
* Button connected to PC13

## Software Requirements

* Rust toolchain
* `probe-run` for flashing and debugging
* A terminal emulator on the host computer

## Building and Running

1. **Clone the repository:** `git clone <repository_url>`
2. **Navigate to the project directory:** `cd audi-can-logger`
3. **Build the project:** `cargo build`
4. **Flash the application:** `probe-run --chip stm32l476rg --defmt flash target/thumbv7em-none-eabihf/debug/mcp2515-embassy`
5. **Connect to the serial port:** Open your terminal emulator and connect to the appropriate serial port (usually detected automatically by `probe-run`).
6. **Interact with the application:**  The application will start in sniffing mode, forwarding CAN messages to the UART. Press and hold the button connected to PC13 to activate SLCAN injection mode. Enter SLCAN formatted messages in the terminal to transmit them on the CAN bus. Release the button to return to sniffing mode.

## SLCAN Usage

The application uses the SLCAN protocol for communication with the host computer.  Here's a quick overview:

* **Transmit:** `t<ID><DATA LENGTH><DATA>` (e.g., `t12348112233445566778`)
* **Receive (displayed by application):** `t<ID><DATA LENGTH><DATA>`

For more details on the SLCAN protocol, refer to [this documentation](https://github.com/linux-can/slcan-docs).


## Code Overview

The core logic resides in the `can_sniffer.rs` file.  Key functionalities include:

* **Initialization:** Initializes the MCP2515 CAN controller with the specified settings (100kbps in this example).
* **CAN message handling:** Reads CAN messages from the MCP2515 and converts them to SLCAN format for transmission over UART.
* **SLCAN message handling:** Parses SLCAN messages received via UART and transmits the corresponding CAN frames using the MCP2515.
* **Button handling:**  Uses the button state to control the operational mode (sniffing or injection).
* **Error handling:** Provides basic error reporting for CAN and UART communication issues.

## Further Development

* **Improved error handling:** Implement more robust error handling and recovery mechanisms.
* **CAN message filtering:** Implement CAN ID filtering to capture specific messages of interest.
* **Data logging:**  Log captured CAN data to a storage device (e.g., SD card).
* **Advanced SLCAN features:** Support additional SLCAN commands for extended functionality.



This README provides a basic overview of the application.  Refer to the source code for more detailed information.