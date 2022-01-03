#!/bin/bash



installDocker()
{
	
	#Setup the repository
	sudo apt-get update
	sudo apt-get install \
	    ca-certificates \
	    curl \
	    gnupg \
	    lsb-release

	#Install GPG Key
	curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

	#Setup Stable Repository
	echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
}


installQuestDB()
{
	docker pull questdb/questdb
	docker run -d -p 9000:9000 questdb/questdb

}
