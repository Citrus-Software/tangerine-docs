---
sidebar_position: 4
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Environment
You will possibly need an environment for your studio, a given production or a group of users.

### User setup
Use TANG_ENV_PATH variable to define the path of a user_setup.py file.
This file will be executing at every launch of Tangerine, before executing another command.

### Custom menus
Tangerine as been developped to be the closest possible of animators needs. Everything you will find native in the software has been optimized in UX and performances way.
Please contact us if you think any of your tools should be part of Tangerine.
That said, you may need to develop some workaround tools to integrate Tangerine in the best way possible for your teams.

You can customize menus, add buttons with preconfigured actions, or even add tools for your teams.
You will find an example in the demo-package.

<details>

  <summary>Add Custom Menus Sample</summary>

    In a Terminal, use for example:
    ```
    SET TANG_ENV_PATH="E:/TEMP/tangerine/Tangerine Demo 2025/api_samples/sample_scripts/"
    "C:\Program Files\TeamTO\Tangerine\1.7.14\TangerineConsole.exe" --log_to_file --kernel release -l debug
    ```
    The user_setup file will execute user_setup script that will create the custom menu develpped in tangerineMenu.py

</details>
