# Kata ansible-vault

Purger les fichiers

```bash
git checkout .
git clean -xdf
```

## Préparation de l'environnement

Montrer ma version ansible

```bash
ansible --version
```

Créer un environnement virtuel pour ansible-2.4

```bash
virtualenv --no-site-packages vansible24
source vansible24/bin/activate
pip install ansible==2.4.6
ansible -version
```

Recharger l'environnement

```bash
deactivate
source vansible24/bin/activate
ansible -version
```

## Première exécution du playbook

* Exécuter le playbook : `ansible-playbook -e @files/extra_vars.yml site.yml`
* Pas besoin d'indiquer l'inventaire : `ansible-config dump`

Explications de ca qui est affiché

## Consultation de la configuration

`ansible-config list`

> Montrer que l'on dispose, pour tous les éléments de configuration, d'une description, du type, de la valeur par défaut ainsi que le nom de la variable d'environnement correspondante et de la variable dans le fichier *ansible.cfg*

## Création d'un vault
