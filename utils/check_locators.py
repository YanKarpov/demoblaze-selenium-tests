import os
import re
import sys
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from locators import (
    MainPageLocators,
    NavigationMenuLocators,
    SignUpModalLocators,
    LoginModalLocators,
    ProductPageLocators,
    CartPageLocators,
)



def get_all_locators():
    """Собирает все локаторы из классов в словарь."""
    locators_classes = {
        "MainPageLocators": MainPageLocators,
        "NavigationMenuLocators": NavigationMenuLocators,
        "SignUpModalLocators": SignUpModalLocators,
        "LoginModalLocators": LoginModalLocators,
        "ProductPageLocators": ProductPageLocators,
        "CartPageLocators": CartPageLocators,
    }
    all_locators = {}
    for class_name, locators_class in locators_classes.items():
        for name, locator in vars(locators_class).items():
            if not name.startswith("__"):
                all_locators[f"{class_name}.{name}"] = locator
    return all_locators


def find_locator_usage(locator_name, search_path="."):
    """Ищет использование локатора в файлах проекта."""
    found_in_files = []
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        if re.search(rf"\b{locator_name}\b", f.read()):
                            found_in_files.append(file_path)
                except Exception as e:
                    print(f"⚠️ Ошибка при чтении {file_path}: {e}")
    return found_in_files


def analyze_locators(search_path):
    """Анализирует локаторы и их использование в коде."""
    all_locators = get_all_locators()
    unused_locators = defaultdict(list)
    used_locators = {}

    for locator_name in all_locators.keys():
        files = find_locator_usage(locator_name, search_path)
        if files:
            used_locators[locator_name] = files
        else:
            class_name = locator_name.split(".")[0]
            unused_locators[class_name].append(locator_name)

    return all_locators, used_locators, unused_locators


def print_results(all_locators, used_locators, unused_locators):
    """Выводит результаты анализа локаторов."""
    print("=" * 50)
    print("🔍 Анализ локаторов завершен.")
    print("=" * 50)

    if used_locators:
        print("\n✅ Используемые локаторы:")
        for locator, files in used_locators.items():
            print(f" - {locator} (найден в {len(files)} файлах)")
            for file in files:
                print(f"    ↳ {file}")

    if unused_locators:
        print("\n⚠️  Неиспользуемые локаторы:")
        for class_name, locators in unused_locators.items():
            print(f"\n🔹 {class_name}:")
            for locator in locators:
                print(f"    - {locator}")

    total_locators = len(all_locators)
    used_count = len(used_locators)
    unused_count = total_locators - used_count
    usage_percentage = (used_count / total_locators) * 100

    print("\n📊 Статистика:")
    print(f" - Всего локаторов: {total_locators}")
    print(f" - Используется: {used_count} ({usage_percentage:.2f}%)")
    print(f" - Не используется: {unused_count}")


if __name__ == "__main__":
    search_path = sys.argv[1] if len(sys.argv) > 1 else "."
    all_locators, used_locators, unused_locators = analyze_locators(search_path)
    print_results(all_locators, used_locators, unused_locators)
