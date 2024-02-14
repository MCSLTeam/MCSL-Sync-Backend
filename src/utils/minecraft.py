class MinecraftVersion(object):
    def __init__(self, version: str) -> None:
        self.major, self.minor, self.patch = self.serialize(version)

    def serialize(self, version) -> tuple[int, int, int]:
        return tuple([int(i) for i in version.replace("v", "").split(".")])

    def __str__(self) -> str:
        return ".".join([str(self.major), str(self.minor), str(self.patch)])
