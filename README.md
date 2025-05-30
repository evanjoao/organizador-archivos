# File Organizer - Advanced Version

An advanced file organization application developed in Python with Tkinter, featuring extended customization, filtering, and change control capabilities.

## 🚀 Main Features

### 🔧 Customizable Configuration Management

- **Custom categories**: Define your own file categories and assign extensions
- **Persistent configuration**: Settings are automatically saved in `settings.json`
- **Intuitive interface**: Dedicated window for managing categories and extensions
- **Category editor**: Add, edit, and delete categories easily

### 🔍 Advanced Filtering System

- **Extension filter**: Select specific file types
- **Size filter**: Define size ranges (KB, MB, GB)
- **Date filter**: Filter by modification or creation date
- **Name filter**: Search by patterns in file names
- **Category filter**: Organize according to custom categories
- **Filter combination**: Use multiple criteria simultaneously

### 👁️ Preview System

- **Detailed preview**: See exactly which files will be moved and where
- **Complete information**: Size, modification date, destination
- **Tree view**: Hierarchical organization of files and destination folders
- **Confirmation before execution**: Prevents organization errors

### ↩️ Undo Operations System

- **Complete history**: Record of all operations performed
- **Selective undo**: Revert specific operations
- **Detailed information**: See which files were moved in each operation
- **Persistence**: History is saved in `undo_history.json`

### 📊 File Statistics

- **Count by category**: How many files of each type
- **Size information**: Space occupied by category
- **Directory analysis**: General view of content
- **Visual distribution**: Clear summary of directory composition

### 🎨 Modern Interface

- Modern and easy-to-use graphical interface (Tkinter + ttk with custom styles)
- Automatic file organization by type
- Support for multiple file types
- Real-time progress visualization
- Detailed operation log with color-coded messages
- Intuitive directory navigation
- Compatible with Windows, Linux, and macOS

## 🎛️ New Interface Controls

### Main Control Buttons

- **Settings**: Opens the category configuration window
- **Filters**: Configures advanced filters for organization
- **Preview**: Shows a preview of changes before applying them
- **Organize**: Executes file organization
- **Undo**: Opens the history window to undo operations
- **Statistics**: Shows detailed directory statistics

### Specialized Windows

#### Settings Window

- List of all available categories
- Buttons to add, edit, and delete categories
- Extension editor for each category
- Automatic saving of changes

#### Filters Window

- Multiple configurable filter types
- Real-time preview of matching files
- Application and clearing of filters
- Combination of criteria

#### Preview Window

- Tree view showing target structure
- Detailed information for each file
- Confirmation before proceeding
- Safe cancellation

#### Undo Window

- Chronological history of operations
- Detailed information for each operation
- Selection and reversal of specific operations
- Validation before undoing

## 📋 System Requirements

- **Python**: 3.6 or higher
- **Tkinter**: Included in most Python installations
- **Operating System**: Windows, Linux, or macOS
- **Disk Space**: Minimal for configuration and history files

## 🔧 Installation

1.**Clone the repository**:

```bash
git clone https://github.com/evanjoao/organizador-archivos.git
cd organizador-archivos
```

2.**Verify Python**:

```bash
python --version  # Should be 3.6+
```

3.**Run the application**:

```bash
python app.py
```

> **Note**: No additional dependencies are required beyond Python and Tkinter.

## 📖 Usage Guide

### 🔰 Basic Usage

1. **Start the application**:

   ```bash
   python app.py
   ```

2. **Select a directory** using the "Browse" button or the directory tree

3. **Organize files**:
   - Click directly on "Organize" to use default settings
   - Or follow the advanced workflow for greater control

### 🎯 Advanced Usage

#### 1. Configure Custom Categories

- Click on **Settings**
- Use "Add Category" to create new categories
- Edit existing categories with "Edit Category"
- Assign specific extensions to each category
- Changes are saved automatically

#### 2. Apply Specific Filters

- Click on **Filters**
- Configure filters by:
  - **Extension**: Select specific types
  - **Size**: Define minimum and maximum ranges
  - **Date**: Filter by modification date
  - **Name**: Use search patterns
  - **Category**: Filter by specific categories
- Apply filters before organizing

#### 3. Preview Changes

- Click on **Preview** after configuring filters
- Review the tree view that shows:
  - Which files will be moved
  - Which folders they will go to
  - Detailed information for each file
- Confirm changes or cancel to adjust

#### 4. Manage Operation History

- Use **Undo** to see all operations performed
- Select specific operations to revert
- View detailed information for each operation
- Confirm before undoing changes

#### 5. Analyze Directories

- Click on **Statistics** to see:
  - File distribution by category
  - Count of files of each type
  - Total size by category
  - General directory summary

## 📁 Project Structure

```text
App/
├── app.py                    # Main application
├── config.py                 # Base configurations and default categories
├── settings_manager.py       # Configuration management system
├── preview_undo.py          # Preview and undo system
├── filters.py               # Advanced filtering system
├── settings.json            # Custom configurations (auto-generated)
├── undo_history.json        # Operation history (auto-generated)
└── README.md               # This file
```

### File Descriptions

- **app.py**: Main file containing the user interface and organization logic
- **config.py**: Default category definitions and basic configurations
- **settings_manager.py**: Custom configuration management and configuration window
- **preview_undo.py**: Preview system and operation history management
- **filters.py**: Advanced filtering system with multiple criteria
- **settings.json**: Auto-generated file to save user configurations
- **undo_history.json**: Auto-generated file to save operation history

## 🗂️ Default Categories

### Documents

- **.pdf, .doc, .docx**: Text documents
- **.txt, .rtf, .odt**: Plain text files and word processors
- **.xls, .xlsx, .ppt, .pptx**: Spreadsheets and presentations

### Images

- **.jpg, .jpeg, .png**: Common image formats
- **.gif, .bmp, .svg**: Additional image formats
- **.webp, .tiff**: Modern image formats

### Videos

- **.mp4, .avi, .mkv**: Popular video formats
- **.mov, .wmv, .flv**: Additional video formats
- **.webm, .m4v**: Modern video formats

### Audio

- **.mp3, .wav, .flac**: Common audio formats
- **.aac, .ogg, .wma**: Additional audio formats
- **.m4a**: Modern audio format

### Compressed Files

- **.zip, .rar, .7z**: Popular compressors
- **.tar, .gz, .bz2**: Unix/Linux compressors

### Code

- **.py, .js, .html, .css**: Web languages and Python
- **.java, .cpp, .c**: Compiled languages
- **.json, .xml, .yaml**: Configuration files

### Executables

- **.exe, .msi**: Windows executables
- **.deb, .rpm**: Linux packages
- **.dmg, .app**: macOS files

## 🛡️ Security Features

- **File validation**: Verification before moving files
- **Operation history**: Complete record to undo changes
- **Preview**: Confirmation before making changes
- **Error handling**: Robust file error management
- **Implicit backups**: The undo system acts as a backup

## 🎨 Customization

### Create Custom Categories

1. Open **Settings**
2. Click on "Add Category"
3. Enter the category name
4. Add extensions separated by commas
5. Confirm to save

### Modify Existing Categories

1. Select a category from the list
2. Click on "Edit Category"
3. Modify the name or extensions
4. Changes are saved automatically

### Delete Categories

1. Select the category to delete
2. Click on "Delete Category"
3. Confirm deletion

## 💡 Usage Tips

### Best Practices

- **Always preview**: Use "Preview" before organizing
- **Configure filters**: To work with specific file types
- **Review history**: The "Undo" button allows you to undo errors
- **Customize categories**: Adapt categories to your needs
- **Keep backups**: Although there's an undo system, backups are important

### Recommended Workflow

1. **Select the directory** to organize
2. **Configure custom categories** if necessary
3. **Apply filters** to work with specific files
4. **Preview** the changes
5. **Execute** the organization
6. **Review** the activity log
7. **Use Statistics** to analyze the result

## 🔮 Future Development

### Planned Features

- **Batch mode**: Organization of multiple directories
- **Cloud integration**: Support for cloud storage services
- **Plugin system**: Custom extensions
- **Additional themes**: More visual customization options
- **Task scheduling**: Scheduled automatic organization
- **Advanced rules**: More complex organization logic

### Contributing

Contributions are welcome. To contribute:

1. **Fork** the project
2. **Create a branch** for your feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

## 📄 License

This project is under the MIT License. See the `LICENSE` file for more details.

## 👨‍💻 Author and Contact

**Evan Joao** - [evanjoaogarciamunoz@gmail.com](mailto:evanjoaogarciamunoz@gmail.com)

**Project Link**: [https://github.com/evanjoao/organizador-archivos](https://github.com/evanjoao/organizador-archivos)

---

### 📊 Enhancement Summary

This advanced version includes:

- ✅ **4 new modules** with specialized functionality
- ✅ **6 new control buttons** in the interface
- ✅ **4 specialized windows** for advanced management
- ✅ **Fully customizable** configuration system
- ✅ **Advanced filters** with multiple criteria
- ✅ **Complete preview** before making changes
- ✅ **Undo system** with persistent history
- ✅ **Detailed statistics** of the directory
- ✅ **Modern and functional** interface

The application has evolved from a basic organizer to a robust and professional tool for file management.
