from appium import webdriver
from dotenv import load_dotenv
import os
from appium.options.android import UiAutomator2Options
import allure
import random

claudio_real_device_samsung = {
    'platformName': 'Android',
    'deviceName': 'R5CW32TQB3F',
    'automationName': 'UiAutomator2',
    'appPackage': "com.amazon.mShop.android.shopping",
    'appActivity': 'com.amazon.mShop.splashscreen.StartupActivity',
    'autoAcceptAlerts': True,
    'autoGrantPermissions': True,
    'noReset': False,
    'fullReset': False,
    'printPageSourceOnFindFailure': True,
    'newCommandTimeout': 800,
    'clearDeviceLogsOnStart': True,
    'clearSystemFiles': True,
    'enforceAppInstall': True
}


def before_all(context):
    load_dotenv()
    if not os.getenv('APP_PASSWORD'):
        raise EnvironmentError("Variable APP_PASSWORD no está definida en .env")


def before_step(context, step):
    print(
        "....................................................................................................................................................")
    print(f"Ejecutando step: {step.name}")
    print(
        "....................................................................................................................................................")


def after_step(context, step):
    print(
        "....................................................................................................................................................")
    print(f"Finalizo Ejecución de step: {step.name}")
    print(
        "....................................................................................................................................................")


def before_scenario(context, scenario):
    # Definir los tags que deben activar el environment
    TAGS_REQUERIDOS = {'smoke_test', 'search_products', 'amazon_login'}

    # Verificar si el escenario tiene alguno de los tags requeridos
    if not any(tag in scenario.tags for tag in TAGS_REQUERIDOS):
        return  # Salir si no tiene los tags requeridos

    print(
        "....................................................................................................................................................")
    print("En ejecucion: " + scenario.name)
    print(f"Tags del escenario: {scenario.tags}")
    print(
        "....................................................................................................................................................")

    appium_server_url = 'http://127.0.0.1:4723/wd/hub'
    capabilities_options = UiAutomator2Options().load_capabilities(claudio_real_device_samsung)
    context.driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)


def after_scenario(context, scenario):
    # Verificar si el escenario tiene los tags requeridos
    TAGS_REQUERIDOS = {'smoke_test', 'search_products', 'amazon_login'}
    if not any(tag in scenario.tags for tag in TAGS_REQUERIDOS):
        return  # Salir si no tiene los tags requeridos

    random_number = random.randint(1, 10000)
    miscreenshotname = "screenshoot" + str(random_number)
    try:
        allure.attach(context.driver.get_screenshot_as_png(), name=miscreenshotname,
                      attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(e)

    # Solo cerrar el driver si fue inicializado
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit()