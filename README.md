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

1. **Set the .env file**:
   - Create a `.env` file in `backend/` folder.
   - Set the following variables:
        ```ini
        DB_URI=
        SECRET=
        GOOGLE_AUTH_CLIENT_ID=
        GOOGLE_OAUTH_CLIENT_SECRET=
        FRONTEND_BASE_URL=
        HF_TOKEN=
        HF_IMG2TXT_MODEL=
        SUPABASE_SERVICE_KEY=
        SUPABASE_URL=
        SUPABASE_BUCKET=
        MAX_IMG_MB_SIZE=
        ```

        For `DB_URI`, you can use the DB container:
        ```ini
        DB_URI="postgresql+asyncpg://postgres:postgres@db:5432/postgres"
        ```

        For `FRONTEND_BASE_URL`, use this URL in development:
        ```ini
        FRONTEND_BASE_URL="http://localhost:5173"
        ```

        For `HF_IMG2TXT_MODEL`, you can use some free models from Hugging Face:
        ```ini
        HF_IMG2TXT_MODEL="meta-llama/Llama-3.2-11B-Vision-Instruct"
        ```

> [!TIP]
> Visit [Hugging Face](https://huggingface.co/docs/hub/security-tokens) to learn to create a token for `HF_TOKEN`.

> [!TIP]
> Visit [OAuth 2.0](https://developers.google.com/identity/protocols/oauth2) to learn how to use Google OAuth 2.0 and set `GOOGLE_AUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET`.

2. **Clone the repository**:
   ```bash
   git clone https://github.com/dmarts05/pixelgram.git
   cd pixelgram
   ```
3. **Open in Dev Container (recommended)**:

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
    8. Open your browser and navigate to [`http://localhost:5173`](http://localhost:5173) to view the frontend app.

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

    6. Open your browser and navigate to [`http://localhost:8000/docs`](http://localhost:8000/docs) to view the backend API.

> [!TIP]
> 🧠 Keep both VS Code windows open — one for the frontend and one for the backend — to work on both services simultaneously.

> [!NOTE]
> 🐳 Make sure Docker is running and both containers can run in parallel on your system.
