
# Runtime Environment & Dependency Boundaries

You are executing inside an ephemeral Docker container launched with the `--rm` flag.
Only files mounted via persistent volumes survive across runs.

## 1. Storage & Persistence Boundaries
- **Project Files (`/workspace`)**: Fully persistent (mounted to host repository).
- **Package Manager Caches (`/root/.npm`, `/usr/local/cargo/registry`)**: Persistent via host cache bind mounts.
- **Credentials & Configurations (`/root/.gemini`)**: Persistent. Contains `Dockerfile.template`.
- **Operating System (`/`, `/usr`, `/lib`, `/etc`)**: NON-PERSISTENT. Erased when the session exits.

## 2. Dependency Resolution Rules
- **Project-Level Tools**: Always install via local repository package managers (`npm`, `cargo`, `pip`) inside `/workspace`.
- **System-Level Dependencies (OS/Compilers/Shared C-C++ Libraries)**:
  - DO NOT read `/root/.gemini/Dockerfile.template` during normal workflow to save context tokens.
  - If a compilation or runtime task fails due to a missing OS-level dependency:
    1. **Stop and Report**: Identify the missing dependency, explain why the current task requires it, and state whether it is a recurring requirement for this tech stack.
    2. **Wait for User Confirmation**: Do NOT install packages or edit files until the user explicitly approves.
    3. **Upon User Approval**:
       - Run the temporary installation command in the current session (e.g., `apt-get install -y <package>`) so the current workflow continues without needing to restart the container.
       - Read `/root/.gemini/Dockerfile.template`, append the required build step cleanly, and save the updated file.