# Kata ansible-vault

Purger les fichiers

```bash
deactivate
git checkout .
git clean -xdf
```

Afficher les pages suivantes :
- [releases](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#release-status)

## Préparation de l'environnement

Montrer ma version ansible

```bash
ansible --version
```

Créer un environnement virtuel pour ansible-2.5.10

```bash
virtualenv --no-site-packages vansible25
source vansible25/bin/activate
pip install ansible==2.5.10
ansible --version
```

Recharger l'environnement

```bash
source vansible25/bin/activate
ansible -version
```

Pourquoi 2.5 ? => [releases](releases)

## Première exécution du playbook

* Exécuter le playbook : `ansible-playbook site.yml`
* Expliquer ce qui est affiché, montrer la variable `NOT DEFINED`
* Exécuter le playbook avec l'extra vars : `ansible-playbook site.yml -e @files/extra_vars.yml`
* Pas besoin d'indiquer l'inventaire avec la conf : `ansible-config dump`
* Ou pour voir les changements : `ansible-config dump --only-changed`

## Commandes ansible-vault

* Afficher le fichier : `cat files/extra_vars.yml`
* Chiffrement du fichier : `ansible-vault encrypt files/extra_vars.yml`
* Afficher le fichier : `cat files/extra_vars.yml`
* Afficher le fichier en clair : `ansible-vault view files/extra_vars.yml`
* Editer le fichier en clair : `ansible-vault edit files/extra_vars.yml`
* Changer le mot de passe du vault : `ansible-vault rekey files/extra_vars.yml`
* Afficher le fichier en clair : `ansible-vault view files/extra_vars.yml`
* Surchiffrement du fichier : `ansible-vault encrypt files/extra_vars.yml` => ERREUR

## Chiffrement d'une string

>TODO

## Utiliser le vault dans un playbook

* Chiffrement du fichier : `ansible-vault encrypt files/extra_vars.yml`
* Exécuter le playbook : `ansible-playbook site.yml -e @files/extra_vars.yml` => ERREUR

### Ansible doit demander le mot de passe

**Via la ligne de commande : --ask-vault-pass**

* `ansible-playbook site.yml -e @files/extra_vars.yml --ask-vault-pass`

**Via la configuration ini : [defaults] ask_vault_pass**

* Rechercher `ask_vault` avec `ansible-config list`

* Ajouter la ligne `ask_vault_pass = True` au fichier *ansible.cfg*
* `ansible-playbook site.yml -e @files/extra_vars.yml`
* Supprimer la ligne `ask_vault_pass = True` du fichier *ansible.cfg*

**Via la variable d'environnement : ANSIBLE_ASK_VAULT_PASS**

* Rechercher `ask_vault` avec `ansible-config list`

* `ANSIBLE_ASK_VAULT_PASS=1 ansible-playbook site.yml -e @files/extra_vars.yml`

### Donner le mot de passe à Ansible

**Via la ligne de commande : --ask-vault-pass**

* `ansible-playbook site.yml -e @files/extra_vars.yml --vault-password-file pass` => ERREUR
* Créer le fichier `echo 1234 > pass`
* `ansible-playbook site.yml -e @files/extra_vars.yml --vault-password-file pass`

**Via une variable dans le playbook**

* `ansible-playbook site.yml -e @files/extra_vars.yml` => ERREUR

Ajouter la ligne suivante dans le playbook :

```yaml
vars:
- defaults:
    vault_password_file: pass
```

**Autres moyens**

env: ANSIBLE_VAULT_PASSWORD_FILE
ini: key: vault_password_file, section: defaults
yaml: key: defaults.vault_password_file



## Consultation de la configuration

`ansible-config list`

> Montrer que l'on dispose, pour tous les éléments de configuration, d'une description, du type, de la valeur par défaut ainsi que le nom de la variable d'environnement correspondante et de la variable dans le fichier *ansible.cfg*

## Création d'un vault
