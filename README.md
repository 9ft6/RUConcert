# RUConcert

RUConcert is a console-based asynchronous parser for retrieving information about concerts and events in Russia. The tool allows you to explore upcoming events, save the data, and stay informed about the vibrant entertainment scene across various Russian regions.

## Features

- Asynchronous parsing for efficient data retrieval.
- Explore concerts and events in different Russian regions.
- Save the parsed results for future reference.

## Getting Started

### Prerequisites

- Python 3.10 or higher

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/RUConcert.git
    cd RUConcert
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage and Configuration

### Running the Parser

To run RUConcert and retrieve information about upcoming events, use the following command:

```bash
python RUConcert.py
```

For more options, customization, and configuration, refer to the available command-line arguments using:


```bash
python RUConcert.py --help
```
To list available regions, use:

```bash
python RUConcert.py --list
```
To parse specific regions, use:


```bash
python RUConcert.py --Moscow --SaintPetersburg
```
To parse all available regions, use:


```bash
python RUConcert.py --all
```
To forcefully update the list of available regions, use:

```bash
python RUConcert.py --update-regions
```

## Final Notes

RUConcert is an open-source project, and your contributions are welcome. Feel free to explore the code, suggest improvements, or report issues. To contribute, please fork the repository, make your changes, and submit a pull request.

We wish you an enjoyable experience using RUConcert and appreciate your interest in making it better!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Disclaimer

RUConcert is a project developed for educational purposes. We do not claim ownership of any external content or data. Any resemblance to real events or locales is entirely coincidental.

