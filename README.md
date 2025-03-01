# SMARTSTUDY-WEBSITE 
<!-- <img src="https://appmaster.io/cdn-cgi/image/width=1024,quality=83,format=auto/api/_files/QsSz55Kp9QZnZyprJbMRcX/download/"> -->

### Deloy - Run with Dockerfile on Window : <hr>
* **Startup Docker and Command Prompt** `(Window + R -> cmd)`:

* **Follows this commands**:

        docker image build -t <name-image> .

* **Check image docker**: 

        docker images 

* **Run container docker (image -> container)**:

        docker run -it --name <container-name> -p <port-run>:8000 
<br>


### Deloy - Run with Dockerfile on Ubuntu: <hr>

**Follows These Commands**

* **Update `APT` source Unbuntu**:
    ```sudo
    sudo apt update
    ```

* **Then add the GPG key for the official Docker repository to your system**:
    ```sudo
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    ```

* **Then add the GPG key for the official Docker repository to your system**:
    ```curl
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

* **Add new Docker Repository to `APT` Source**:
    ```sudo
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
    ```
* **Install Docker**:
    ```sudo
    sudo apt install docker-ce
    ```

* **After the above step, `Docker` was installed, `deamon` will startup (Docker Service runs in the background) and `Process` will be added in boot (startup with system). To check if the `Docker Deamon` has been started, we use the following command**:
    ```sudo
    sudo systemctl status docker
    ```
    **Output**:
    ```
    ● docker.service - Docker Application Container Engine
        Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
        Active: active (running) since Tue 2020-05-19 17:00:41 UTC; 17s ago
    TriggeredBy: ● docker.socket
        Docs: https://docs.docker.com
    Main PID: 24321 (dockerd)
        Tasks: 8
        Memory: 46.4M
        CGroup: /system.slice/docker.service
                └─24321 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
    ```

* **Finally, use command**:
    ```
    sudo docker-compose up 
    ```