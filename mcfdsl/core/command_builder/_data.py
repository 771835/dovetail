# coding=utf-8
MINECRAFT_VERSION = ["1.20.4"]


class Data:
    # --------------------------
    # data get 命令
    # --------------------------
    @staticmethod
    def get_block(target_pos: str, path: str = None, scale: float = None):
        cmd = f"data get block {target_pos}"
        if path:
            cmd += f" {path}"
        if scale is not None:
            cmd += f" {scale}"
        return cmd

    @staticmethod
    def get_entity(target: str, path: str = None, scale: float = None):
        cmd = f"data get entity {target}"
        if path:
            cmd += f" {path}"
        if scale is not None:
            cmd += f" {scale}"
        return cmd

    @staticmethod
    def get_storage(target: str, path: str = None, scale: float = None):
        cmd = f"data get storage {target}"
        if path:
            cmd += f" {path}"
        if scale is not None:
            cmd += f" {scale}"
        return cmd

    # --------------------------
    # data merge 命令
    # --------------------------
    @staticmethod
    def merge_block(target_pos: str, nbt: str):
        """Merges NBT data into a block at target_pos."""
        return f"data merge block {target_pos} {nbt}"

    @staticmethod
    def merge_entity(target: str, nbt: str):
        """Merges NBT data into an entity."""
        return f"data merge entity {target} {nbt}"

    @staticmethod
    def merge_storage(target: str, nbt: str):
        """Merges NBT data into a storage."""
        return f"data merge storage {target} {nbt}"

    # --------------------------
    # data modify 命令
    # --------------------------

    # Helper to build modify command strings
    @staticmethod
    def _build_modify_command(
            target_type: str,
            target: str,
            target_path: str,
            operation: str,
            source_part: str):
        """Builds the base data modify command string."""
        return f"data modify {target_type} {target} {target_path} {operation} {source_part}"

    # --- append ---
    @staticmethod
    def modify_block_append_from_block(
            target_pos: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Appends NBT data from a source block to a target block's list."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "append", source_part)

    @staticmethod
    def modify_block_append_from_entity(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Appends NBT data from a source entity to a target block's list."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "append", source_part)

    @staticmethod
    def modify_block_append_from_storage(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Appends NBT data from a source storage to a target block's list."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "append", source_part)

    @staticmethod
    def modify_block_append_string_block(
            target_pos: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source block to a target block's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "append", source_part)

    @staticmethod
    def modify_block_append_string_entity(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source entity to a target block's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "append", source_part)

    @staticmethod
    def modify_block_append_string_storage(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source storage to a target block's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "append", source_part)

    @staticmethod
    def modify_block_append_value(
            target_pos: str,
            target_path: str,
            value: str):
        """Appends a specific NBT value to a target block's list."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "append", source_part)

    # --- insert ---
    @staticmethod
    def modify_block_insert_from_block(
            target_pos: str,
            target_path: str,
            index: int,
            source_pos: str,
            source_path: str = None):
        """Inserts NBT data from a source block into a target block's list at index."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block",
            target_pos,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_block_insert_from_entity(
            target_pos: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None):
        """Inserts NBT data from a source entity into a target block's list at index."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block",
            target_pos,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_block_insert_from_storage(
            target_pos: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None):
        """Inserts NBT data from a source storage into a target block's list at index."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block",
            target_pos,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_block_insert_string_block(
            target_pos: str,
            target_path: str,
            index: int,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source block into a target block's string at index."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block",
            target_pos,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_block_insert_string_entity(
            target_pos: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source entity into a target block's string at index."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block",
            target_pos,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_block_insert_string_storage(
            target_pos: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source storage into a target block's string at index."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block",
            target_pos,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_block_insert_value(
            target_pos: str,
            target_path: str,
            index: int,
            value: str):
        """Inserts a specific NBT value into a target block's list at index."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "block",
            target_pos,
            target_path,
            f"insert {index}",
            source_part)

    # --- merge ---
    @staticmethod
    def modify_block_merge_from_block(
            target_pos: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Merges NBT data from a source block into a target block."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "merge", source_part)

    @staticmethod
    def modify_block_merge_from_entity(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Merges NBT data from a source entity into a target block."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "merge", source_part)

    @staticmethod
    def modify_block_merge_from_storage(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Merges NBT data from a source storage into a target block."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "merge", source_part)

    @staticmethod
    def modify_block_merge_string_block(
            target_pos: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source block into a target block's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "merge", source_part)

    @staticmethod
    def modify_block_merge_string_entity(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source entity into a target block's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "merge", source_part)

    @staticmethod
    def modify_block_merge_string_storage(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source storage into a target block's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "merge", source_part)

    @staticmethod
    def modify_block_merge_value(
            target_pos: str,
            target_path: str,
            value: str):
        """Merges a specific NBT value into a target block."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "merge", source_part)

    # --- prepend ---
    @staticmethod
    def modify_block_prepend_from_block(
            target_pos: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Prepends NBT data from a source block to a target block's list."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "prepend", source_part)

    @staticmethod
    def modify_block_prepend_from_entity(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Prepends NBT data from a source entity to a target block's list."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "prepend", source_part)

    @staticmethod
    def modify_block_prepend_from_storage(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Prepends NBT data from a source storage to a target block's list."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "prepend", source_part)

    @staticmethod
    def modify_block_prepend_string_block(
            target_pos: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source block to a target block's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "prepend", source_part)

    @staticmethod
    def modify_block_prepend_string_entity(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source entity to a target block's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "prepend", source_part)

    @staticmethod
    def modify_block_prepend_string_storage(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source storage to a target block's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "prepend", source_part)

    @staticmethod
    def modify_block_prepend_value(
            target_pos: str,
            target_path: str,
            value: str):
        """Prepends a specific NBT value to a target block's list."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "prepend", source_part)

    # --- set ---
    @staticmethod
    def modify_block_set_from_block(
            target_pos: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Sets NBT data from a source block to a target block."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "set", source_part)

    @staticmethod
    def modify_block_set_from_entity(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Sets NBT data from a source entity to a target block."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "set", source_part)

    @staticmethod
    def modify_block_set_from_storage(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Sets NBT data from a source storage to a target block."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "set", source_part)

    @staticmethod
    def modify_block_set_string_block(
            target_pos: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source block to a target block's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "set", source_part)

    @staticmethod
    def modify_block_set_string_entity(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source entity to a target block's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "set", source_part)

    @staticmethod
    def modify_block_set_string_storage(
            target_pos: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source storage to a target block's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "set", source_part)

    @staticmethod
    def modify_block_set_value(target_pos: str, target_path: str, value: str):
        """Sets a specific NBT value to a target block."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "block", target_pos, target_path, "set", source_part)

    # --- Entity Modify ---

    # --- append ---
    @staticmethod
    def modify_entity_append_from_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Appends NBT data from a source block to a target entity's list."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "append", source_part)

    @staticmethod
    def modify_entity_append_from_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Appends NBT data from a source entity to a target entity's list."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "append", source_part)

    @staticmethod
    def modify_entity_append_from_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Appends NBT data from a source storage to a target entity's list."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "append", source_part)

    @staticmethod
    def modify_entity_append_string_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source block to a target entity's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "append", source_part)

    @staticmethod
    def modify_entity_append_string_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source entity to a target entity's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "append", source_part)

    @staticmethod
    def modify_entity_append_string_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source storage to a target entity's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "append", source_part)

    @staticmethod
    def modify_entity_append_value(target: str, target_path: str, value: str):
        """Appends a specific NBT value to a target entity's list."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "entity", target, target_path, "append", source_part)

    # --- insert ---
    @staticmethod
    def modify_entity_insert_from_block(
            target: str,
            target_path: str,
            index: int,
            source_pos: str,
            source_path: str = None):
        """Inserts NBT data from a source block into a target entity's list at index."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, f"insert {index}", source_part)

    @staticmethod
    def modify_entity_insert_from_entity(
            target: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None):
        """Inserts NBT data from a source entity into a target entity's list at index."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, f"insert {index}", source_part)

    @staticmethod
    def modify_entity_insert_from_storage(
            target: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None):
        """Inserts NBT data from a source storage into a target entity's list at index."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, f"insert {index}", source_part)

    @staticmethod
    def modify_entity_insert_string_block(
            target: str,
            target_path: str,
            index: int,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source block into a target entity's string at index."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, f"insert {index}", source_part)

    @staticmethod
    def modify_entity_insert_string_entity(
            target: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source entity into a target entity's string at index."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, f"insert {index}", source_part)

    @staticmethod
    def modify_entity_insert_string_storage(
            target: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source storage into a target entity's string at index."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, f"insert {index}", source_part)

    @staticmethod
    def modify_entity_insert_value(
            target: str,
            target_path: str,
            index: int,
            value: str):
        """Inserts a specific NBT value into a target entity's list at index."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "entity", target, target_path, f"insert {index}", source_part)

    # --- merge ---
    @staticmethod
    def modify_entity_merge_from_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Merges NBT data from a source block into a target entity."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "merge", source_part)

    @staticmethod
    def modify_entity_merge_from_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Merges NBT data from a source entity into a target entity."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "merge", source_part)

    @staticmethod
    def modify_entity_merge_from_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Merges NBT data from a source storage into a target entity."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "merge", source_part)

    @staticmethod
    def modify_entity_merge_string_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source block into a target entity's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "merge", source_part)

    @staticmethod
    def modify_entity_merge_string_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source entity into a target entity's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "merge", source_part)

    @staticmethod
    def modify_entity_merge_string_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source storage into a target entity's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "merge", source_part)

    @staticmethod
    def modify_entity_merge_value(target: str, target_path: str, value: str):
        """Merges a specific NBT value into a target entity."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "entity", target, target_path, "merge", source_part)

    # --- prepend ---
    @staticmethod
    def modify_entity_prepend_from_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Prepends NBT data from a source block to a target entity's list."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_entity_prepend_from_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Prepends NBT data from a source entity to a target entity's list."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_entity_prepend_from_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Prepends NBT data from a source storage to a target entity's list."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_entity_prepend_string_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source block to a target entity's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_entity_prepend_string_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source entity to a target entity's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_entity_prepend_string_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source storage to a target entity's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_entity_prepend_value(target: str, target_path: str, value: str):
        """Prepends a specific NBT value to a target entity's list."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "entity", target, target_path, "prepend", source_part)

    # --- set ---
    @staticmethod
    def modify_entity_set_from_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Sets NBT data from a source block to a target entity."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "set", source_part)

    @staticmethod
    def modify_entity_set_from_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Sets NBT data from a source entity to a target entity."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "set", source_part)

    @staticmethod
    def modify_entity_set_from_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Sets NBT data from a source storage to a target entity."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "entity", target, target_path, "set", source_part)

    @staticmethod
    def modify_entity_set_string_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source block to a target entity's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "set", source_part)

    @staticmethod
    def modify_entity_set_string_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source entity to a target entity's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "set", source_part)

    @staticmethod
    def modify_entity_set_string_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source storage to a target entity's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "entity", target, target_path, "set", source_part)

    @staticmethod
    def modify_entity_set_value(target: str, target_path: str, value: str):
        """Sets a specific NBT value to a target entity."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "entity", target, target_path, "set", source_part)

    # --- Storage Modify ---

    # --- append ---
    @staticmethod
    def modify_storage_append_from_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Appends NBT data from a source block to a target storage's list."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "append", source_part)

    @staticmethod
    def modify_storage_append_from_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Appends NBT data from a source entity to a target storage's list."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "append", source_part)

    @staticmethod
    def modify_storage_append_from_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Appends NBT data from a source storage to a target storage's list."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "append", source_part)

    @staticmethod
    def modify_storage_append_string_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source block to a target storage's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "append", source_part)

    @staticmethod
    def modify_storage_append_string_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source entity to a target storage's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "append", source_part)

    @staticmethod
    def modify_storage_append_string_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Appends string data from a source storage to a target storage's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "append", source_part)

    @staticmethod
    def modify_storage_append_value(target: str, target_path: str, value: str):
        """Appends a specific NBT value to a target storage's list."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "storage", target, target_path, "append", source_part)

    # --- insert ---
    @staticmethod
    def modify_storage_insert_from_block(
            target: str,
            target_path: str,
            index: int,
            source_pos: str,
            source_path: str = None):
        """Inserts NBT data from a source block into a target storage's list at index."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage",
            target,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_storage_insert_from_entity(
            target: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None):
        """Inserts NBT data from a source entity into a target storage's list at index."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage",
            target,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_storage_insert_from_storage(
            target: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None):
        """Inserts NBT data from a source storage into a target storage's list at index."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage",
            target,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_storage_insert_string_block(
            target: str,
            target_path: str,
            index: int,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source block into a target storage's string at index."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage",
            target,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_storage_insert_string_entity(
            target: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source entity into a target storage's string at index."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage",
            target,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_storage_insert_string_storage(
            target: str,
            target_path: str,
            index: int,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Inserts string data from a source storage into a target storage's string at index."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage",
            target,
            target_path,
            f"insert {index}",
            source_part)

    @staticmethod
    def modify_storage_insert_value(
            target: str,
            target_path: str,
            index: int,
            value: str):
        """Inserts a specific NBT value into a target storage's list at index."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "storage",
            target,
            target_path,
            f"insert {index}",
            source_part)

    # --- merge ---
    @staticmethod
    def modify_storage_merge_from_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Merges NBT data from a source block into a target storage."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "merge", source_part)

    @staticmethod
    def modify_storage_merge_from_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Merges NBT data from a source entity into a target storage."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "merge", source_part)

    @staticmethod
    def modify_storage_merge_from_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Merges NBT data from a source storage into a target storage."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "merge", source_part)

    @staticmethod
    def modify_storage_merge_string_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source block into a target storage's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "merge", source_part)

    @staticmethod
    def modify_storage_merge_string_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source entity into a target storage's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "merge", source_part)

    @staticmethod
    def modify_storage_merge_string_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Merges string data from a source storage into a target storage's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "merge", source_part)

    @staticmethod
    def modify_storage_merge_value(target: str, target_path: str, value: str):
        """Merges a specific NBT value into a target storage."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "storage", target, target_path, "merge", source_part)

    # --- prepend ---
    @staticmethod
    def modify_storage_prepend_from_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Prepends NBT data from a source block to a target storage's list."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_storage_prepend_from_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Prepends NBT data from a source entity to a target storage's list."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_storage_prepend_from_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Prepends NBT data from a source storage to a target storage's list."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_storage_prepend_string_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source block to a target storage's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_storage_prepend_string_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source entity to a target storage's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_storage_prepend_string_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Prepends string data from a source storage to a target storage's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "prepend", source_part)

    @staticmethod
    def modify_storage_prepend_value(
            target: str,
            target_path: str,
            value: str):
        """Prepends a specific NBT value to a target storage's list."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "storage", target, target_path, "prepend", source_part)

    # --- set ---
    @staticmethod
    def modify_storage_set_from_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None):
        """Sets NBT data from a source block to a target storage."""
        source_part = f"from block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "set", source_part)

    @staticmethod
    def modify_storage_set_from_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Sets NBT data from a source entity to a target storage."""
        source_part = f"from entity {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "set", source_part)

    @staticmethod
    def modify_storage_set_from_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None):
        """Sets NBT data from a source storage to a target storage."""
        source_part = f"from storage {source}"
        if source_path:
            source_part += f" {source_path}"
        return Data._build_modify_command(
            "storage", target, target_path, "set", source_part)

    @staticmethod
    def modify_storage_set_string_block(
            target: str,
            target_path: str,
            source_pos: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source block to a target storage's string."""
        source_part = f"string block {source_pos}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "set", source_part)

    @staticmethod
    def modify_storage_set_string_entity(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source entity to a target storage's string."""
        source_part = f"string entity {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "set", source_part)

    @staticmethod
    def modify_storage_set_string_storage(
            target: str,
            target_path: str,
            source: str,
            source_path: str = None,
            start: int = None,
            end: int = None):
        """Sets string data from a source storage to a target storage's string."""
        source_part = f"string storage {source}"
        if source_path:
            source_part += f" {source_path}"
        if start is not None:
            source_part += f" {start}"
            if end is not None:
                source_part += f" {end}"
        return Data._build_modify_command(
            "storage", target, target_path, "set", source_part)

    @staticmethod
    def modify_storage_set_value(target: str, target_path: str, value: str):
        """Sets a specific NBT value to a target storage."""
        source_part = f"value {value}"
        return Data._build_modify_command(
            "storage", target, target_path, "set", source_part)

    # --------------------------
    # data remove 命令
    # --------------------------
    @staticmethod
    def remove_block(target_pos: str, path: str):
        """Removes NBT data at a path from a block."""
        return f"data remove block {target_pos} {path}"

    @staticmethod
    def remove_entity(target: str, path: str):
        """Removes NBT data at a path from an entity."""
        return f"data remove entity {target} {path}"

    @staticmethod
    def remove_storage(target: str, path: str):
        """Removes NBT data at a path from a storage."""
        return f"data remove storage {target} {path}"
