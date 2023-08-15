import os
import json

sql_string ="""
CREATE TABLE `auth_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `scopes` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_roles-name-un` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
name = 'phonebook'
definitions = {
    "module": f"pabx_{name}",
    "resource": f"{name}",
    'root_dir':os.path.dirname(os.path.abspath(__file__)),
    "infra":{
        "pkgs":{
            "sql_string":sql_string,
            "tab_name":"",
            "tab_owner":""
        }
    }
}
