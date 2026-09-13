terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "meteorites-rg"
  location = "West Europe"
}

resource "azurerm_container_registry" "acr" {
  name                = "meteoritesibrahim"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}
resource "azurerm_container_group" "app" {
  name                = "meteorites-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  ip_address_type     = "Public"
  dns_name_label      = "meteoritesibrahim"

  image_registry_credential {
    server   = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }

  container {
    name   = "meteorites-app"
    image  = "${azurerm_container_registry.acr.login_server}/meteorites-app:latest"
    cpu    = "0.5"
    memory = "1"

    ports {
      port     = 5000
      protocol = "TCP"
    }
  }
}

output "app_url" {
  value = "http://${azurerm_container_group.app.fqdn}:5000"
}