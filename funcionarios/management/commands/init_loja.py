from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from funcionarios.models import Cargo


class Command(BaseCommand):
    help = "Inicializa os Cargos/Grupos padrão e o Superusuário da Loja JBS"

    def handle(self, *args, **options):
        cargos_padrao = [
            ("Administrador Geral", "Acesso total a todos os módulos do sistema"),
            ("Gerente de Loja", "Gestão de caixa, relatórios financeiros e estoque"),
            ("Operador de Caixas", "Abertura/Fechamento de caixa e sangrias"),
            ("Vendedor / Balcão", "Realização de vendas no PDV e consulta de produtos"),
            ("Estoquista / Compras", "Entrada de notas, cadastro e reposição de produtos"),
            ("Motorista / Entregador", "Visualização e confirmação de entregas na rota"),
        ]

        self.stdout.write("🔧 Criando Cargos e Grupos de Permissões...")

        for nome_cargo, descricao in cargos_padrao:
            grupo, _ = Group.objects.get_or_create(name=f"Grupo_{nome_cargo.replace(' ', '_')}")
            cargo, created = Cargo.objects.get_or_create(
                nome=nome_cargo,
                defaults={"grupo_django": grupo, "descricao": descricao}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  - Cargo '{nome_cargo}' criado."))
            else:
                self.stdout.write(f"  - Cargo '{nome_cargo}' já existe.")

        # Criar Superusuário Padrão de Desenvolvimento
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@lojajbs.com.br", "admin123")
            self.stdout.write(self.style.SUCCESS("🚀 Superusuário 'admin' (senha: admin123) criado!"))
        else:
            self.stdout.write("ℹ️ Superusuário 'admin' já existe.")