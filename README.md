# pixelgram


[![Visit Pixelgram](https://img.shields.io/badge/Visit%20Pixelgram-Live%20App-blue?style=for-the-badge&logo=rocket)](https://pixelgram-frontend-gmxf.onrender.com/)


Pixelgram is a web app which allows users to create, publish and share Pixel Arts, as well as interact with other creations through comments and “likes”, all in a visual environment similar to that of social networks such as Instagram.
It includes tools such as an interactive canvas, automatic generation of descriptions using AI, and the ability to import images to convert them into Pixel Art.

## ✨ Features

- 🎨 **Interactive Canvas**: A user-friendly interface for creating pixel art.
- 🖼️ **Image Import**: Convert images into pixel art.
- 🤖 **AI Description Generation**: Automatically generate descriptions for your pixel art.
- 💬 **Social Interaction**: Like, comment and save any creations.
- 👤 **User Profiles**: Create and manage your own profile.
- 📱 **Responsive Design**: Optimized for both desktop and mobile devices.
- 🔐 **User Authentication**: Secure login and registration system. OAuth 2.0 support.

## ⚙️ Development Environment

This project supports development with Dev Containers for a consistent setup across environments.

### Prerequisites
- Docker (for devcontainer)

### Setting Up the Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dmarts05/pixelgram.git
   cd pixelgram
   ```
2. **Open in Dev Container (recommended)**:

   Pixelgram uses **two separate Dev Containers** for development: one for the `frontend` and one for the `backend`. Each folder contains its own `.devcontainer` configuration.

   To work with them:

   #### 🔧 Open the Frontend Dev Container

   1. Open **Visual Studio Code**.
   2. Navigate to the `frontend/` folder.
   3. If you have the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed, VS Code will prompt you to reopen in a container.
   4. Or, open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run:
    ```VS Code
    Dev Containers: Reopen in Container
    ```
    5. Wait for the container to build and start. This may take a few minutes, especially the first time.
    6. Install dependencies:
       ```bash
       bun install
       ```
    7. Start the development server:
       ```bash
        bun dev
        ```
    8. Open your browser and navigate to `http://localhost:5173` to view the frontend app.

   #### 🔧 Open the Backend Dev Container

   1. Open a **new VS Code window**.
   2. Navigate to the `backend/` folder.
   3. Reopen this folder in a Dev Container using the same steps as above.
   4. Install dependencies:
      ```bash
      uv sync
      ```
    5. Start the development server:
        - Click the debug button in VS Code and select `Python Debugger: FastAPI`.
        - Or type in terminal:
            ```bash
            uvicorn pixelgram.__main__:app --reload
            ```
    6. Open your browser and navigate to `http://localhost:8000/docs` to view the backend API.


   > 🧠 **Tip**: Keep both VS Code windows open — one for the frontend and one for the backend — to work on both services simultaneously.

   > 🐳 **Note**: Make sure Docker is running and both containers can run in parallel on your system.