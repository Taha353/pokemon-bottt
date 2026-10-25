import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random


class Pokemon:
    pokemons = {}

    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(50, 100)
        self.power = random.randint(10, 20)

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["forms"][0]["name"]
                return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return (
            f"Pokémonunuzun ismi: {self.name} | Canı (HP): {self.hp} | "
            f"Gücü: {self.power}"
        )

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            sans = random.randint(1, 5)
            if sans == 1:
                return (
                    f"@{enemy.pokemon_trainer} un Sihirbaz Pokémonu savaşta "
                    "sihirli bir kalkan kullandı ve saldırıyı savuşturdu! "
                    "Hiç hasar almadı."
                )

        if enemy.hp > self.power:
            enemy.hp -= self.power
            return (
                f"Pokémon eğitmeni @{self.pokemon_trainer}, "
                f"@{enemy.pokemon_trainer}'ne saldırdı.\n"
                f"@{enemy.pokemon_trainer}'nin yeni sağlık durumu: {enemy.hp}"
            )

        enemy.hp = 0
        self.hp += 20
        self.power += 5
        return (
            f"Pokémon eğitmeni @{self.pokemon_trainer}, "
            f"@{enemy.pokemon_trainer}'ni yendi! 🏆\n"
            "Bonus kazandınız! "
            f"Yeni Can: {self.hp}, Yeni Güç: {self.power}"
        )

    async def show_img(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["sprites"]["front_default"]
                return None


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = random.randint(100, 150)
        self.power = random.randint(8, 15)

    async def info(self):
        base_info = await super().info()
        return f"✨ Sihirbaz Pokémonunuz var! ✨\n{base_info}"


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = random.randint(60, 90)
        self.power = random.randint(20, 35)

    async def attack(self, enemy):
        super_guc = random.randint(5, 15)
        self.power += super_guc
        sonuc = await super().attack(enemy)
        self.power -= super_guc
        return (
            sonuc + f"\n💥 Dövüşçü Pokémon süper saldırı kullandı! "
            f"Eklenen güç: {super_guc}"
        )

    async def info(self):
        base_info = await super().info()
        return f"⚔️ Dövüşçü Pokémonunuz var! ⚔️\n{base_info}"
                