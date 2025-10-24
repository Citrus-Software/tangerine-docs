---
sidebar_position: 5
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Command Line Arguments

You can use scripting in GUI mode or in batch mode.

`GUI Mode` : The main mode launch the application with main window only. These following code example are using this GUI Mode, using methods that will take in charge UI aspects (refreshing viewport, showing progres, etc).
@sixtine log View available

`GUI Console Mode` : A "console" mode with main window and console window is available to have verbosity and can be usefull in your developments.

`Batch Mode` : The batch mode of tangerine is also available. Every methods that are linked to the UI application part won't be available in this mode. See our code example in "batch" page to adapt your scripts to batch mode. See [Batch mode guide](command_line#batch-mode).

### UI Mode

To launch Tangerine in UI mode, use the following command:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --log_to_file --kernel release
```

If you want to enable monitoring, replace the `--log_to_file` flag with `--monitoring`:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --kernel release
```

---

### Batch Mode

To launch Tangerine in Batch mode, use the following command:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --log_to_file --no-hidden --no-gui --kernel release
```

If you want to enable monitoring, use:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release
```

---

### Script Execution

You can append the path to one or more Python scripts directly in the command line:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe --monitoring --no-hidden --no-gui --kernel release example.tang my_python_script.py
```

Scripts will be executed **in order**. If a listed script does not exist, Tangerine will simply skip it.

---

Find in the demo package sample scripts to help you test command line

```
"E:/TEMP/tangerine/Tangerine Demo 2025/Tangerine/TangerineConsole.exe" --log_to_file --kernel release -l debug --no-hidden --no-gui "E:/TEMP/tangerine/Tangerine Demo 2025/after_opening_tangerine.py" "E:/TEMP/tangerine/Tangerine Demo 2025/hook.py" "E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/three_capy.shot" "E:/TEMP/tangerine/Tangerine Demo 2025/after_loading_document.py"
```
![console tangerine](./img/console_batch_tangerine.png)


### Help

For more details about the Tangerine command line, run:

```bash
c:/"program files"/Tangerine/tangerineConsole.exe -h
```
