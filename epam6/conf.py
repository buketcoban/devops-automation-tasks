import yaml
from jinja2 import Environment, FileSystemLoader


def main():
    with open("data.yml") as f:
        data = yaml.safe_load(f)
    
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("vhosts.j2")
    
    rendered = template.render(vhosts=data["vhosts"])
    
    with open("vhosts.conf", "w") as f:
        f.write(rendered)


if __name__ == "__main__":
    main()