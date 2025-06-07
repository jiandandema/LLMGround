from enum import Enum


class ModelType(str, Enum):
    EMBED = "embed"
    CLASSIFY = "classify"
    REWARD = "reward"
    SCORE = "score"
    GENERATE = "generate"
