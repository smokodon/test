# Use the official Windows Server Core image
FROM mcr.microsoft.com/windows/servercore:ltsc2022
SHELL ["powershell", "-Command"]
# Install Visual Studio Build Tools
RUN Invoke-WebRequest -Uri https://aka.ms/vs/17/release/vs_buildtools.exe -OutFile vs_buildtools.exe ; \
    Start-Process -Wait -FilePath vs_buildtools.exe -ArgumentList '--quiet', '--wait', '--norestart', '--nocache', '--installPath', 'C:\\BuildTools', '--add', 'Microsoft.VisualStudio.Workload.VCTools' ; \
    Remove-Item -Force vs_buildtools.exe

# Install WSL
RUN Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-2004 -OutFile Ubuntu.appx ; \
    Add-AppxPackage .\Ubuntu.appx ; \
    wsl --set-default-version 2

# Set the entrypoint to WSL
ENTRYPOINT ["wsl.exe", "-d", "Ubuntu-20.04", "--", "bash", "-c", "echo Hello from WSL"]
