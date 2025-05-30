# File Organizer

A desktop application developed in Python to automatically organize files into folders by type.

## Features

- Modern and easy-to-use graphical interface (Tkinter + ttk, custom styles)
- Automatic file organization by type
- Support for multiple file types
- Real-time progress visualization
- Detailed operation log with color-coded messages
- Intuitive directory navigation (directory tree, custom selection)
- Compatible with Windows, Linux, and macOS

## Requirements

- Python 3.x
- tkinter (included in most Python installations)
- Operating system: Windows, Linux, or macOS

## Installation

1. Clone this repository:

```bash
git clone https://github.com/evanjoao/organizador-archivos.git
cd organizador-archivos
```

2. Install dependencies (if you have requirements.txt):

```bash
pip install -r requirements.txt
```

> **Note:** If there is no `requirements.txt`, just make sure you have Python 3 and tkinter installed.

## Usage

1. Run the application:

```bash
python app.py
```

2. Select the directory you want to organize
3. Click on "Organize Files"
4. Wait for the process to complete
5. Check the activity log for details

## Project Structure

```
organizador-archivos/
├── app.py              # Main application (Tkinter)
├── config.py           # Visual configuration and constants
├── requirements.txt    # Project dependencies (optional)
├── LICENSE             # MIT License
└── README.md           # This file
```

## Recent Changes

- Complete migration to Tkinter and ttk for a modern, cross-platform visual experience
- Improved directory tree and log area visualization
- Color-coded log messages (info, success, warning, error)
- Improved organization and responsive interface design

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is under the MIT License. See the `LICENSE` file for more details.

## Author & Contact

Evan Joao - [evanjoaogarciamunoz@gmail.com](mailto:evanjoaogarciamunoz@gmail.com)

Project Link: [https://github.com/evanjoao/organizador-archivos](https://github.com/evanjoao/organizador-archivos)
