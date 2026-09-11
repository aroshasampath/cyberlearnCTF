from pathlib import Path
import secrets


env_file = Path(__file__).with_name(".env")

if env_file.exists():
    print(".env already exists. No changes were made.")
    raise SystemExit()


content = f"""SECRET_KEY={secrets.token_hex(32)}
FLAG_PEPPER={secrets.token_hex(32)}

STAGE1_FLAG=GROUP18{{hidden_metadata_found}}
STAGE2_FLAG=GROUP18{{client_side_gate_broken}}
STAGE3_FLAG=GROUP18{{double_layer_decoded}}
STAGE4_FLAG=GROUP18{{digital_footprints_traced}}
STAGE5_FLAG=GROUP18{{traffic_stream_identified}}
STAGE6_FLAG=GROUP18{{root_of_the_problem}}
"""


env_file.write_text(content, encoding="utf-8")

print(".env created successfully.")