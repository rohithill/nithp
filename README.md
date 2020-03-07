# NITH Projects
A repo containing multiple projects relating to NIT Hamirpur. 

#### Current list:
- NITH Result Website
- NITH Result API

Built using python3, flask, connexion, bootstrap. Virtual environment is managed using [pipenv](https://github.com/pypa/pipenv).

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Please make sure that python version >= 3.7.

Open the terminal and run the following commands:

1. Clone the repository
```bash
$ git clone https://github.com/rohithill/nithp.git
$ cd nithp
```
2. Create the virtual environment and install dependencies
```bash
$ pipenv install
```
3. Enter into shell
```bash
$ pipenv shell
```
4. Run the application 
```bash
$ flask run
```

### Todo
- [x] Make a interface for simple users to view their result.
- [x] Implement a basic API to get results.
- [x] Implement pagination in the API.
- [ ] Add examples on how to use API in various cases.


### Branches
**master :**  All the changes are made in the master. All the pull requests are merged here finally.

**deploy :** This is the branch which is deployed to the website. Currently the deploy is automatic. All the push to this branch are deployed immediately.

### Notes
- To ssh through heroku-cli, `heroku run bash`
- https://kb.sites.apiit.edu.my/knowledge-base/how-to-gzip-response-in-flask/
  
