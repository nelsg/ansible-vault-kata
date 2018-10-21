# Kata ansible-vault

* Purger les fichiers
  ```bash
  deactivate
  git checkout .
  git clean -xdf
  ```

* Afficher les pages suivantes :
  * [releases](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#release-status)

## Préparation de l'environnement

* Montrer ma version ansible : `ansible --version`
* Créer un environnement virtuel pour ansible-2.5.10
  ```bash
  virtualenv --no-site-packages vansible25
  source vansible25/bin/activate
  pip install ansible==2.5.10
  ansible --version
  ```
* Recharger l'environnement
  ```bash
  source vansible25/bin/activate
  ansible -version
  ```
* Pourquoi 2.5 ? => [releases](releases)

## Première exécution du playbook

* Exécuter le playbook : `ansible-playbook site.yml`
* Expliquer ce qui est affiché, montrer la variable `NOT DEFINED`
* Exécuter le playbook avec l'extra vars : `ansible-playbook site.yml -e @files/extra_vars.yml`
* Pas besoin d'indiquer l'inventaire avec la conf : `ansible-config dump`
* Où pour voir les changements : `ansible-config dump --only-changed`

## Commandes de base de `ansible-vault`

Séries de commandes pour manipuler les vaults avec la commande `ansible-vault` : chiffrement, déchiffrement, affichage, édition et changement de mot de passe.

* Afficher le fichier : `cat files/extra_vars.yml`
* Chiffrement du fichier : `ansible-vault encrypt files/extra_vars.yml`
* Afficher le fichier : `cat files/extra_vars.yml`
* Afficher le fichier en clair : `ansible-vault view files/extra_vars.yml`
* Editer le fichier en clair : `ansible-vault edit files/extra_vars.yml`
* Changer le mot de passe du vault : `ansible-vault rekey files/extra_vars.yml`
* Afficher le fichier en clair : `ansible-vault view files/extra_vars.yml`
* Surchiffrement du fichier : `ansible-vault encrypt files/extra_vars.yml` => ERREUR
* Remettre le mot de passe initial : `ansible-vault rekey files/extra_vars.yml`
* Afficher les arguments de `ansible-vault` : `ansible-vault --help`

## Utiliser le vault avec un playbook

Comment utiliser votre vault avec les outils ansible comme les commandes `ansible`, `ansible-playbook`, etc.

* Chiffrement du fichier : `ansible-vault encrypt files/extra_vars.yml`
* Exécuter le playbook : `ansible-playbook site.yml -e @files/extra_vars.yml` => ERREUR

### Ansible doit demander le mot de passe

**Via la ligne de commande : --ask-vault-pass**

* `ansible-playbook site.yml -e @files/extra_vars.yml --ask-vault-pass`

**Via la configuration ini : [defaults] ask_vault_pass**

* Rechercher `ask_vault_pass` avec `ansible-config list`
* Ajouter la ligne `ask_vault_pass = True` au fichier *ansible.cfg*
* Exécuter le playbook : `ansible-playbook site.yml -e @files/extra_vars.yml`
* Supprimer la ligne `ask_vault_pass = True` du fichier *ansible.cfg*

**Via la variable d'environnement : ANSIBLE_ASK_VAULT_PASS**

* Rechercher `ask_vault_pass` avec `ansible-config list`
* On peut aussi utiliser une variable d'environnement `ANSIBLE_ASK_VAULT_PASS=1 ansible-playbook site.yml -e @files/extra_vars.yml`

### Donner le mot de passe à Ansible dans un fichier

**Via la ligne de commande : --vault-password-file**

* `ansible-playbook site.yml -e @files/extra_vars.yml --vault-password-file pass` => ERREUR
* Créer le fichier `echo 1234 > pass`
* `ansible-playbook site.yml -e @files/extra_vars.yml --vault-password-file pass`

**Autres moyens**

* Variable d'environnement : `env: ANSIBLE_VAULT_PASSWORD_FILE`
* Paramètre dans le fichier *ansible.cfg* : `ini: key: vault_password_file, section: defaults`
* Paramètre yaml : `yaml: key: defaults.vault_password_file`

### Donner le mot de passe à Ansible dans un script python

>TODO : Voir comment le mettre en place

## Chiffrement d'une string

Chiffre un fichier complet n'est pas forcément pertinent. Une solution peut être d'avoir deux fichiers dont l'un est chiffré. Une autre approche est de chiffrer partiellement un fichier. C'est ce que nous permet de faire la commande `encrypt_string` de l'outil `ansible-vault`.

* On veut chiffrer uniquement le champ du fichier *files/vars_files.yml*
* Affichage : `cat files/vars_files.yml`
* Chiffrement d'une valeur depuis la ligne de commande : `ansible-vault encrypt_string "vars_files DEFINED encrypted"`
* Avec le nom : `ansible-vault encrypt_string "vars_files DEFINED encrypted" --name 'my_vars_files_value'`
* On donne le fichier contenant le mot de passe :
  `ansible-vault encrypt_string "vars_files DEFINED encrypted" --name 'my_vars_files_value' --vault-password-file pass`
* Prendre le contenu et la mettre dans le fichier *files/vars_files.yml*
* Ansible reconnait l'entête `!vault |` et déchiffre ce qui suit
* Exécuter le playbook : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-password-file pass`
* L'argorithme utilise ce que l'on appelle une fonction de salage, cela permet de renforcer la sécurité des informations en ajoutant une donnée qui permet d'éviter d'avoir la même empreinte. Le but est de compliquer les attaques s'appuyant sur l'analyse fréquentielle, la force brute
* Exécuter plusieurs fois la commande :
  `ansible-vault encrypt_string "vars_files DEFINED encrypted" --name 'my_vars_files_value' --vault-password-file pass`

**Autres moyens de chiffrement**

* Depuis *stdin* :
`echo -n "vars_files DEFINED encrypted" | ansible-vault encrypt_string --stdin-name 'my_vars_files_value' --vault-password-file pass`

## Chiffrement avec un mot de passe différent

Si vous ne l'avez pas remarqué, j'utilise le même mot de passe depuis le début, comment faire si l'on a un deuxième mot de passe à gérer ?

* Chiffrement du fichier *files/include_vars.yml* : `ansible-vault encrypt files/include_vars.yml`
* Exécution du playbook : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-password-file pass` => ERREUR
* Demande du mot de passe en plus : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-password-file pass --ask-vault-pass` => ERREUR
* Demande du mot de passe seul : `ansible-playbook site.yml -e @files/extra_vars.yml --ask-vault-pass` => ERREUR

### Utilisation de l'argument vault-id

* Pour résoudre le problème ci-dessus, on utilise l'argument `--vault-id`
* On peut en utiliser autant que l'on veut, il faut voir cet argument comme un moyen de fournir un ou plusieurs mots de passe à ansible
* Par exemple, demander la saisie de deux mot de passe : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id @prompt --vault-id @prompt`
* Le `@prompt` demande à ansible de demander un mot de passe
* Si pas de `@`, c'est interprété comme un nom de fichier
* Créer un fichier avec l'autre mot de passe : `echo azerty > pass2`
* L'utiliser dans la ligne de commande : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id pass --vault-id pass2`
* L'ordre n'a pas d'importance : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id pass2 --vault-id pass`
* On peut vraiment empiler les mots de passe. Ansible utilise tous les mots de passe dont il dispose pour déchiffrer : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id pass --vault-id pass2 --vault-id @prompt`
* Il essaye toutes les mots de passe, dans l'ordre de saisie dans la ligne de commande, jusqu'à en trouver un qui fonctionne

### Avec le fichier *ansible.cfg*

* Regardons comment utiliser vault-id : `ansible-config list`
* Rechercher `vault_identity_list` : on peut utiliser une variable d'environnement, un yaml ou dans le fichier ini. Le type est une liste
* Ajout dans le fichier de configuration : `echo "vault_identity_list=pass,pass2" >> ansible.cfg`
* On peut exécuter le playbook comme initialement : `ansible-playbook site.yml -e @files/extra_vars.yml`
* On peut utiliser également des `@prompt` dans *ansible.cfg*

## Utilisation des clés pour les vault-id

Les `vault-id` ont été introduits avec la version 2.4 d'ansible. C'est d'ailleurs devenu la manière officielle de fournir des mots de passe, exit dont `--ask-vault-pass` et `--vault-password-file`.

On a vu que l'on pouvait en utiliser plusieurs `vault-id` et qu'ansible effectue des tentatives par force brute.
Voyons comment amméliorer cela.

* Préparation en supprimant les fichiers de mots de passes
* Restaurer la conf : `git checkout .`

### Chiffrer les données :

**Chiffrement du fichier extra**

* Chiffrer le fichier *files/extra_vars.yml* comme avant, mais avec le `vault-id` : `ansible-vault encrypt --vault-id @prompt files/extra_vars.yml`
* Afficher le fichier : `cat files/extra_vars.yml`
* Déchiffrer : `ansible-vault decrypt --vault-id @prompt files/extra_vars.yml`
* Chiffer à nouveau, mais avec la clé `extra` : `ansible-vault encrypt --vault-id demo@prompt files/extra_vars.yml`
* Afficher le fichier : `cat files/extra_vars.yml`
* La version est passé de `1.1` à `1.2` et on trouve la clé `demo` dans le fichier
* Placer le mot de passe dans le fichier *pass_demo* : `echo 1234 >> pass_demo`

**Chiffrement de la valeur dans le fichier vars**

* Chiffrer la chaine `vars_files` de caractère avec la clé `demo` et le mot de passe dans le fichier : `ansible-vault encrypt_string "vars_files DEFINED encrypted" --name 'my_vars_files_value' --vault-id demo@pass_demo`
* Essayer le playbook : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id demo@pass_demo`

**Chiffrement du fichier include**

* Créer le fichier *pass_vault* : `echo azerty >> pass_vault`
* Chiffrer le fichier : `ansible-vault encrypt --vault-id vault@pass_vault files/include_vars.yml`
* Essayer le playbook : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id demo@pass_demo --vault-id vault@pass_vault`

Mais j'ai menti, ça marche aussi avec :
* `--vault-id pass_demo --vault-id pass_vault`
* `--vault-id toto@pass_demo --vault-id tata@pass_vault`
* `--vault-id toto@pass_demo --vault-id toto@pass_vault`

**Associer la clé au vault**

* Regarder `vault_id_match` dans `ansible-config list`
* L'ajouter dans *ansible.cfg* : `echo "vault_id_match=1" >> ansible.cfg`
* Maintenant, seul fonctionne : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id demo@pass_demo --vault-id vault@pass_vault`

## Chiffrement de tous les fichiers

* Chiffrer le fichier *group_vars/all.yml* : `ansible-vault encrypt --vault-id vault@pass_vault group_vars/all.yml`
* Chiffrer le fichier *files/certificat.cer* : `ansible-vault encrypt --vault-id demo@pass_demo files/certificat.cer`
* Chiffrement du default du rôle *roles/kata/defaults/main.yml* : `ansible-vault encrypt --vault-id vault@pass_vault roles/kata/defaults/main.yml`

* On essaye : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id pass_demo --vault-id pass_vault`

* On continue : `ansible-vault encrypt --vault-id demo@pass_demo roles/kata/tasks/main.yml`
* Ca fonctionne ..

* Et le playbook ? : `ansible-vault encrypt --vault-id demo@pass_demo site.yml`
* Ca fonctionne ..

* On peut tout chiffrer, sauf *ansible.cfg*

## Utilisation de scripts pour les vault-id

* Restaure tout : `git checkout .`
* Chiffrement du fichier `files/extra_vars.yml` : `ansible-vault encrypt --vault-id vault@pass_demo files/extra_vars.yml`
* Editez le fichier `pass_demo` et mettre :
  ```python
  #!/usr/bin/python
  print("1234")
  ```
* On essaye : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id pass_demo` => ERREUR
* On ajoute les droits d'exécution : `chmod +x pass_demo`
* On essaye : `ansible-playbook site.yml -e @files/extra_vars.yml --vault-id pass_demo` => OK

### Que mettre dans le script
