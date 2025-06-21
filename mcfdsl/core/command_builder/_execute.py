# coding=utf-8
from typing import List, Literal, Optional

# Define Literal types for better type hinting and potential validation
# Note: Some of these Literals are based on common Minecraft usage,
#       not strictly limited by the provided tree snippet which is simplified.
Axes = Literal["x", "y", "z", "xy", "xz", "yz",
               "xyz", "yx", "yzx", "zy", "zxy", "zyx"]
Anchor = Literal["eyes", "feet"]
OnRelationship = Literal["attacker",
                         "controller",
                         "leasher",
                         "origin",
                         "owner",
                         "passengers",
                         "target",
                         "vehicle"]
HeightmapType = Literal["motion_blocking",
                        "motion_blocking_no_leaves",
                        "ocean_floor",
                        "world_surface"]
BlocksMode = Literal["all", "masked"]
# Added more score operations based on common MCJE syntax
# [ "+=", "-=", "*=", "/=", "%=", "<=>"]
ScoreOperation = Literal["=", "<", "<=", ">", ">="]
# Added the full list of valid numeric NBT types for 'store'
StoreType = Literal["int", "float", "short", "long", "double", "byte"]
BossbarStoreType = Literal["value", "max"]


class ExecuteBuilder:
    """
    A builder class for constructing Minecraft Java Edition execute commands.
    Chain methods to add subcommands, then call .run() to finalize.
    """

    def __init__(self, parts: Optional[List[str]] = None):
        # Start with "execute"
        self._parts: List[str] = parts if parts is not None else ["execute"]

    def _add_part(self, part: str) -> 'ExecuteBuilder':
        """Helper to add a part to the command and return self for chaining."""
        self._parts.append(part)
        return self

    # --------------------------
    # Context Modifiers (return self for chaining)
    # --------------------------

    def align(self, axes: Axes) -> 'ExecuteBuilder':
        """
        Aligns the execution position to the block grid on the specified axes.

        Args:
            axes: A string of characters 'x', 'y', 'z' indicating axes to align.
        """
        return self._add_part(f"align {axes}")

    def anchored(self, anchor: Anchor) -> 'ExecuteBuilder':
        """
        Changes the execution position based on the entity's anchor (eyes or feet).

        Args:
            anchor: 'eyes' or 'feet'.
        """
        return self._add_part(f"anchored {anchor}")

    def as_(self, targets: str) -> 'ExecuteBuilder':
        """
        Changes the execution entity.

        Args:
            targets: A target selector or player name.
        """
        return self._add_part(f"as {targets}")

    def at(self, targets: str) -> 'ExecuteBuilder':
        """
        Changes the execution position and rotation to that of the target(s).

        Args:
            targets: A target selector or player name.
        """
        return self._add_part(f"at {targets}")

    def facing(self, pos: str) -> 'ExecuteBuilder':
        """
        Changes the execution rotation to face a specific position.

        Args:
            pos: A position (e.g., "~ ~ ~" or "10 64 -5").
        """
        return self._add_part(f"facing {pos}")

    def facing_entity(self, targets: str, anchor: Anchor) -> 'ExecuteBuilder':
        """
        Changes the execution rotation to face an entity's anchor (eyes or feet).

        Args:
            targets: A target selector or player name.
            anchor: 'eyes' or 'feet'.
        """
        return self._add_part(f"facing entity {targets} {anchor}")

    def in_dimension(self, dimension: str) -> 'ExecuteBuilder':
        """
        Changes the execution dimension.

        Args:
            dimension: The dimension ID (e.g., "minecraft:overworld", "minecraft:the_nether", "minecraft:the_end").
        """
        return self._add_part(f"in {dimension}")

    def on(self, relationship: OnRelationship) -> 'ExecuteBuilder':
        """
        Changes the execution entity to a related entity.

        Args:
            relationship: The relationship type (e.g., 'vehicle', 'passengers', 'owner').
        """
        return self._add_part(f"on {relationship}")

    def positioned(self, pos: str) -> 'ExecuteBuilder':
        """
        Changes the execution position.

        Args:
            pos: A position (e.g., "~ ~ ~" or "10 64 -5").
        """
        return self._add_part(f"positioned {pos}")

    def positioned_as(self, targets: str) -> 'ExecuteBuilder':
        """
        Changes the execution position to that of the target(s).
        (Based on typical MCJE syntax, interpreting 'positioned ... as <targets>' from tree)

        Args:
            targets: A target selector or player name.
        """
        return self._add_part(f"positioned as {targets}")

    def positioned_over(self, heightmap: HeightmapType) -> 'ExecuteBuilder':
        """
        Changes the execution position to the highest block according to a heightmap.

        Args:
            heightmap: The type of heightmap to use.
        """
        return self._add_part(f"positioned over {heightmap}")

    def rotated(self, rot: str) -> 'ExecuteBuilder':
        """
        Changes the execution rotation.

        Args:
            rot: A rotation string (e.g., "~ ~" or "0 90").
        """
        return self._add_part(f"rotated {rot}")

    def rotated_as(self, targets: str) -> 'ExecuteBuilder':
        """
        Changes the execution rotation to that of the target(s).
        (Based on typical MCJE syntax, interpreting 'rotated ... as <targets>' from tree)

        Args:
            targets: A target selector or player name.
        """
        return self._add_part(f"rotated as {targets}")

    # --------------------------
    # Conditional Branches (if/unless - return self)
    # --------------------------

    def _add_conditional_part(self,
                              condition_type: Literal["if",
                                                      "unless"],
                              part: str) -> 'ExecuteBuilder':
        """Helper to add an if or unless part and return self."""
        return self._add_part(f"{condition_type} {part}")

    def if_biome(self, pos: str, biome: str) -> 'ExecuteBuilder':
        """Tests for a specific biome at a position."""
        return self._add_conditional_part("if", f"biome {pos} {biome}")

    def unless_biome(self, pos: str, biome: str) -> 'ExecuteBuilder':
        """Tests if a specific biome is NOT present at a position."""
        return self._add_conditional_part("unless", f"biome {pos} {biome}")

    def if_block(self, pos: str, block: str) -> 'ExecuteBuilder':
        """Tests for a specific block (including states/NBT) at a position."""
        return self._add_conditional_part("if", f"block {pos} {block}")

    def unless_block(self, pos: str, block: str) -> 'ExecuteBuilder':
        """Tests if a specific block is NOT present at a position."""
        return self._add_conditional_part("unless", f"block {pos} {block}")

    def if_blocks(
            self,
            start: str,
            end: str,
            destination: str,
            mode: BlocksMode) -> 'ExecuteBuilder':
        """Compares two block regions (start...end with destination origin)."""
        return self._add_conditional_part(
            "if", f"blocks {start} {end} {destination} {mode}")

    def unless_blocks(
            self,
            start: str,
            end: str,
            destination: str,
            mode: BlocksMode) -> 'ExecuteBuilder':
        """Tests if two block regions do NOT match."""
        return self._add_conditional_part(
            "unless", f"blocks {start} {end} {destination} {mode}")

    # Data conditions
    def if_data_block(self, source_pos: str, path: str) -> 'ExecuteBuilder':
        """Tests for the existence of NBT data at a specific path on a block."""
        return self._add_conditional_part(
            "if", f"data block {source_pos} {path}")

    def unless_data_block(
            self,
            source_pos: str,
            path: str) -> 'ExecuteBuilder':
        """Tests for the non-existence of NBT data at a specific path on a block."""
        return self._add_conditional_part(
            "unless", f"data block {source_pos} {path}")

    def if_data_entity(self, source: str, path: str) -> 'ExecuteBuilder':
        """Tests for the existence of NBT data at a specific path on an entity."""
        return self._add_conditional_part("if", f"data entity {source} {path}")

    def unless_data_entity(self, source: str, path: str) -> 'ExecuteBuilder':
        """Tests for the non-existence of NBT data at a specific path on an entity."""
        return self._add_conditional_part(
            "unless", f"data entity {source} {path}")

    def if_data_storage(self, source: str, path: str) -> 'ExecuteBuilder':
        """Tests for the existence of NBT data at a specific path in a storage."""
        return self._add_conditional_part(
            "if", f"data storage {source} {path}")

    def unless_data_storage(self, source: str, path: str) -> 'ExecuteBuilder':
        """Tests for the non-existence of NBT data at a specific path in a storage."""
        return self._add_conditional_part(
            "unless", f"data storage {source} {path}")

    def if_dimension(self, dimension: str) -> 'ExecuteBuilder':
        """Tests if the execution is currently in a specific dimension."""
        return self._add_conditional_part("if", f"dimension {dimension}")

    def unless_dimension(self, dimension: str) -> 'ExecuteBuilder':
        """Tests if the execution is currently NOT in a specific dimension."""
        return self._add_conditional_part("unless", f"dimension {dimension}")

    def if_entity(self, entities: str) -> 'ExecuteBuilder':
        """Tests for the existence of entity/entities matching the selector."""
        return self._add_conditional_part("if", f"entity {entities}")

    def unless_entity(self, entities: str) -> 'ExecuteBuilder':
        """Tests for the non-existence of entity/entities matching the selector."""
        return self._add_conditional_part("unless", f"entity {entities}")

    def if_function(self, name: str) -> 'ExecuteBuilder':
        """Tests the success of running a function (return code 1)."""
        return self._add_conditional_part("if", f"function {name}")

    def unless_function(self, name: str) -> 'ExecuteBuilder':
        """Tests the failure of running a function (return code 0)."""
        return self._add_conditional_part("unless", f"function {name}")

    # Item conditions
    def if_items_block(
            self,
            pos: str,
            slots: str,
            item_predicate: str) -> 'ExecuteBuilder':
        """Tests for items matching a predicate in a block inventory slot(s)."""
        return self._add_conditional_part(
            "if", f"items block {pos} {slots} {item_predicate}")

    def unless_items_block(
            self,
            pos: str,
            slots: str,
            item_predicate: str) -> 'ExecuteBuilder':
        """Tests for the absence of items matching a predicate in a block inventory slot(s)."""
        return self._add_conditional_part(
            "unless", f"items block {pos} {slots} {item_predicate}")

    def if_items_entity(
            self,
            entities: str,
            slots: str,
            item_predicate: str) -> 'ExecuteBuilder':
        """Tests for items matching a predicate in an entity inventory slot(s)."""
        return self._add_conditional_part(
            "if", f"items entity {entities} {slots} {item_predicate}")

    def unless_items_entity(
            self,
            entities: str,
            slots: str,
            item_predicate: str) -> 'ExecuteBuilder':
        """Tests for the absence of items matching a predicate in an entity inventory slot(s)."""
        return self._add_conditional_part(
            "unless", f"items entity {entities} {slots} {item_predicate}")

    def if_loaded(self, pos: str) -> 'ExecuteBuilder':
        """Tests if the chunk at the specified position is loaded."""
        return self._add_conditional_part("if", f"loaded {pos}")

    def unless_loaded(self, pos: str) -> 'ExecuteBuilder':
        """Tests if the chunk at the specified position is NOT loaded."""
        return self._add_conditional_part("unless", f"loaded {pos}")

    def if_predicate(self, predicate: str) -> 'ExecuteBuilder':
        """Tests a registered predicate."""
        return self._add_conditional_part("if", f"predicate {predicate}")

    def unless_predicate(self, predicate: str) -> 'ExecuteBuilder':
        """Tests if a registered predicate is NOT met."""
        return self._add_conditional_part("unless", f"predicate {predicate}")

    # Score conditions
    def if_score_compare(
            self,
            target: str,
            target_objective: str,
            operation: ScoreOperation,
            source: str,
            source_objective: str) -> 'ExecuteBuilder':
        """Compares two scores."""
        return self._add_conditional_part(
            "if",
            f"score {target} {target_objective} {operation} {source} {source_objective}")

    def unless_score_compare(
            self,
            target: str,
            target_objective: str,
            operation: ScoreOperation,
            source: str,
            source_objective: str) -> 'ExecuteBuilder':
        """Tests if two scores do NOT match the comparison."""
        return self._add_conditional_part(
            "unless",
            f"score {target} {target_objective} {operation} {source} {source_objective}")

    def if_score_matches(
            self,
            target: str,
            target_objective: str,
            range_: str) -> 'ExecuteBuilder':
        """Tests if a score matches a numerical range."""
        # Using range_ because 'range' is a built-in function in Python
        return self._add_conditional_part(
            "if", f"score {target} {target_objective} matches {range_}")

    def unless_score_matches(
            self,
            target: str,
            target_objective: str,
            range_: str) -> 'ExecuteBuilder':
        """Tests if a score does NOT match a numerical range."""
        return self._add_conditional_part(
            "unless", f"score {target} {target_objective} matches {range_}")

    # --------------------------
    # Store Branches (store result/success - return self)
    # --------------------------

    def _add_store_part(self,
                        store_type: Literal["result",
                                            "success"],
                        part: str) -> 'ExecuteBuilder':
        """Helper to add a store part and return self."""
        return self._add_part(f"store {store_type} {part}")

    # store block
    def store_result_block(
            self,
            target_pos: str,
            path: str,
            store_type: StoreType,
            scale: float) -> 'ExecuteBuilder':
        """Stores the numerical result of the command into a block's NBT."""
        return self._add_store_part(
            "result", f"block {target_pos} {path} {store_type} {scale}")

    def store_success_block(
            self,
            target_pos: str,
            path: str,
            store_type: StoreType,
            scale: float) -> 'ExecuteBuilder':
        """Stores the success of the command (1 or 0) into a block's NBT."""
        return self._add_store_part(
            "success", f"block {target_pos} {path} {store_type} {scale}")

    # store bossbar
    def store_result_bossbar(
            self,
            id_: str,
            bossbar_store_type: BossbarStoreType) -> 'ExecuteBuilder':
        """Stores the numerical result of the command into a bossbar's value or max."""
        return self._add_store_part("result", f"bossbar {id_} {bossbar_store_type}")

    def store_success_bossbar(
            self,
            id_: str,
            bossbar_store_type: BossbarStoreType) -> 'ExecuteBuilder':
        """Stores the success of the command (1 or 0) into a bossbar's value or max."""
        return self._add_store_part("success", f"bossbar {id_} {bossbar_store_type}")

    # store entity
    def store_result_entity(
            self,
            target: str,
            path: str,
            store_type: StoreType,
            scale: float) -> 'ExecuteBuilder':
        """Stores the numerical result of the command into an entity's NBT."""
        return self._add_store_part(
            "result", f"entity {target} {path} {store_type} {scale}")

    def store_success_entity(
            self,
            target: str,
            path: str,
            store_type: StoreType,
            scale: float) -> 'ExecuteBuilder':
        """Stores the success of the command (1 or 0) into an entity's NBT."""
        return self._add_store_part(
            "success", f"entity {target} {path} {store_type} {scale}")

    # store score
    def store_result_score(
            self,
            targets: str,
            objective: str) -> 'ExecuteBuilder':
        """Stores the numerical result of the command into a score."""
        return self._add_store_part("result", f"score {targets} {objective}")

    def store_success_score(
            self,
            targets: str,
            objective: str) -> 'ExecuteBuilder':
        """Stores the success of the command (1 or 0) into a score."""
        return self._add_store_part("success", f"score {targets} {objective}")

    # store storage
    def store_result_storage(
            self,
            target: str,
            path: str,
            store_type: StoreType,
            scale: float) -> 'ExecuteBuilder':
        """Stores the numerical result of the command into a storage's NBT."""
        return self._add_store_part(
            "result", f"storage {target} {path} {store_type} {scale}")

    def store_success_storage(
            self,
            target: str,
            path: str,
            store_type: StoreType,
            scale: float) -> 'ExecuteBuilder':
        """Stores the success of the command (1 or 0) into a storage's NBT."""
        return self._add_store_part(
            "success", f"storage {target} {path} {store_type} {scale}")

    # --------------------------
    # Final Command
    # --------------------------

    def run(self, command: str) -> str:
        """
        Specifies the command to run and finalizes the execute command string.

        Args:
            command: The command string to execute.

        Returns:
            The complete execute command string.
        """
        self._parts.append(f"run {command}")
        return " ".join(self._parts)

    # Alias for __str__ to allow printing the command at any stage (useful for
    # debugging)
    def __str__(self) -> str:
        return " ".join(self._parts)

    def __repr__(self) -> str:
        return f"ExecuteBuilder(parts={self._parts!r})"


class Execute:
    """
    Static class for starting a Minecraft Java Edition execute command chain.
    Use Execute.execute() to begin building a command.
    """
    @staticmethod
    def execute() -> ExecuteBuilder:
        """Starts building an execute command chain."""
        return ExecuteBuilder()
