## Recipe 00
The recipe demonstrates how to use Ray to evaluate AI agents at scale. 

### References
* [Ray: What’s Ray Core?](https://docs.ray.io/en/latest/ray-core/walkthrough.html)

## Part 00
This part of the recipe outlines the setup for this project. 

**Step 1.** Install `kubectl`.
```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg 
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
```

**Step 2.** Install `kind`. 
```bash
go install sigs.k8s.io/kind@v0.30.0
```

**Step 3.** Open your shell's runtime configuration file. 
```bash
vim .bashrc
```

**Step 4.** Update your execution path so it includes your local Go `bin` directory (where `kind` was installed). 
```bash
export PATH="$(go env GOPATH)/bin:$PATH"
```

**Step 5.** Run the provided script. A kubeconfig will be automatically merged into `~/.kube/config`.
```bash
bash build-cluster-and-regisry.sh
```

```
Unable to find image 'registry:2' locally
2: Pulling from library/registry
44cf07d57ee4: Pull complete 
bbbdd6c6894b: Pull complete 
8e82f80af0de: Pull complete 
3493bf46cdec: Pull complete 
6d464ea18732: Pull complete 
Digest: sha256:a3d8aaa63ed8681a604f1dea0aa03f100d5895b6a58ace528858a7b332415373
Status: Downloaded newer image for registry:2
7d0faa41630a80caf7ba03030f352e21d1fe30b93da4e0e627418a6d35d6b022
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.34.0) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a nice day! 👋
configmap/local-registry-hosting created
```

**Step 6.** Text goes here.
```bash
docker image ls
```

```
REPOSITORY                             TAG       IMAGE ID       CREATED        SIZE
kindest/node                           <none>    4357c93ef232   2 months ago   985MB
registry                               2         26b2eb03618e   2 years ago    25.4MB
```

**Step 7.** Text goes here.
```bash
docker image ls 
```

**Step 8.** Text goes here.
```bash
git clone https://github.com/xbow-engineering/validation-benchmarks.git
rm -rf validation-benchmarks/.git
```

**Step 9.** Text goes here.
```bash
cd validation-benchmarks
make build BENCHMARK=XBEN-001-24
```

**Step 10.** Text goes here.
```bash
docker tag xben-001-24-idor_broken_authz_trading_platform:latest localhost:5001/app:latest
docker tag xben-001-24-db:latest localhost:5001/db:latest
```

**Step 11.** Text goes here.
```bash
docker push localhost:5001/app:latest
docker push localhost:5001/db:latest
```

**Step 12.** Text goes here.
```bash
curl -s http://localhost:5001/v2/_catalog
```

```json
{
  "repositories": [
    "app",
    "db"
  ]
}
```

**Step 13.** Text goes here.
```
kubectl apply -f target-01.yml
```

**Step 14.** Text goes here.
```bash
kubectl port-forward svc/app 8000:80
```

## Part 01
This part of the recipe outlines the setup for this project. 

**Step 1.** Create a Python virtual environment. 
```bash
python -m venv .venv
```

**Step 2.** Activate the Python virtual environment you just created. 
```bash
source .venv/bin/activate
```

**Step 3.** Create a file called `requirements.txt` and add the content below to it. The file will be used to identify this project's Python dependencies. 
```bash
ray
```

**Step 4.** Install this project's Python dependencies. 
```bash
python -m pip install -r requirements.txt
```

**Step 5.** If you are using VS Code as your code editor, now would be a good time to select the Python interpreter within your virtual environment as your default Python interpreter. This will make it easier to write and debug your code as you follow along with this recipe. 

## Part 02
This part of the recipe will confirm your local development is setup correctly. 

**Step 1.** Create a file called `main.py` and add the content below to it. 
```python
import ray

ray.init()
```

**Step 2.** Use the Python interpreter to run your code. 
```bash
python main.py
```