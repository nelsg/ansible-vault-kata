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
ansible -version
```

Recharger l'environnement

```bash
source vansible25/bin/activate
ansible -version
```

Pourquoi 2.5 ? => [releases](releases)

## Première exécution du playbook

* Exécuter le playbook : `ansible-playbook site.yml`
* Pas besoin d'indiquer l'inventaire : `ansible-config dump`
* Exécuter le playbook avec l'extra vars : `ansible-playbook site.yml -e @files/extra_vars.yml`

Explications de ce qui est affiché

## Consultation de la configuration

`ansible-config list`

> Montrer que l'on dispose, pour tous les éléments de configuration, d'une description, du type, de la valeur par défaut ainsi que le nom de la variable d'environnement correspondante et de la variable dans le fichier *ansible.cfg*

## Création d'un vault
