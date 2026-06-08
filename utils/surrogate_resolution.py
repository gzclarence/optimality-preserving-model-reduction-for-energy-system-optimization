"""
Time clustering utilities for surrogate modeling.
"""


def build_time_clusters(n_clusters: int):
    """
    Generate time clusters for a given number of clusters.

    Parameters
    ----------
    n_clusters : int
        Number of time clusters (e.g., 365, 730, 1460, 8760)

    Returns
    -------
    list_of_clusters : list[list[int]]
        Each element is a list of hours belonging to that cluster.
    """

    if n_clusters == 4:
        return [
            list(range(1, 2161)),
            list(range(2161, 4345)),
            list(range(4345, 6553)),
            list(range(6553, 8761)),
        ]

    if n_clusters == 12:
        return [
            list(range(1, 745)),
            list(range(745, 1417)),
            list(range(1417, 2161)),
            list(range(2161, 2881)),
            list(range(2881, 3625)),
            list(range(3625, 4345)),
            list(range(4345, 5089)),
            list(range(5089, 5833)),
            list(range(5833, 6553)),
            list(range(6553, 7297)),
            list(range(7297, 8017)),
            list(range(8017, 8761)),
        ]

    if n_clusters == 59:
        # Weekly clusters (5 weeks every month)
        return [range(1,169),range(169,337),range(337,505),range(505,673),range(673,745),\
                     range(745,913),range(913,1081),range(1081,1249),range(1249,1417),\
                     range(1417,1585),range(1585,1753),range(1753,1921),range(1921,2089),range(2089,2161),\
                     range(2161,2161+168),range(2161+168,2161+2*168),range(2161+2*168,2161+3*168),range(2161+3*168,2161+4*168),range(2161+4*168,2881),\
                     range(2881,2881+168),range(2881+168,2881+2*168),range(2881+2*168,2881+3*168),range(2881+3*168,2881+4*168),range(2881+4*168,3625),\
                     range(3625,3625+168),range(3625+168,3625+2*168),range(3625+2*168,3625+3*168),range(3625+3*168,3625+4*168),range(3625+4*168,4345),\
                     range(4345,4345+168),range(4345+168,4345+2*168),range(4345+2*168,4345+3*168),range(4345+3*168,4345+4*168),range(4345+4*168,5089),\
                     range(5089,5089+168),range(5089+168,5089+2*168),range(5089+2*168,5089+3*168),range(5089+3*168,5089+4*168),range(5089+4*168,5833),\
                     range(5833,5833+168),range(5833+168,5833+2*168),range(5833+2*168,5833+3*168),range(5833+3*168,5833+4*168),range(5833+4*168,6553),\
                     range(6553,6553+168),range(6553+168,6553+2*168),range(6553+2*168,6553+3*168),range(6553+3*168,6553+4*168),range(6553+4*168,7297),\
                     range(7297,7297+168),range(7297+168,7297+2*168),range(7297+2*168,7297+3*168),range(7297+3*168,7297+4*168),range(7297+4*168,8017),\
                     range(8017,8017+168),range(8017+168,8017+2*168),range(8017+2*168,8017+3*168),range(8017+3*168,8017+4*168),range(8017+4*168,8761)]

    if n_clusters == 365:
        # Daily clusters
        return [
            list(range((d - 1) * 24 + 1, d * 24 + 1))
            for d in range(1, 366)
        ]

    if n_clusters == 365 * 3:
        # 8-hour clusters
        clusters = []
        for d in range(1, 366):
            base = (d - 1) * 24
            for i in range(3):
                start = base + i * 8 + 1
                end = base + (i + 1) * 8 + 1
                clusters.append(list(range(start, end)))
        return clusters

    if n_clusters == 365 * 6:
        # 4-hour clusters
        clusters = []
        for d in range(1, 366):
            base = (d - 1) * 24
            for i in range(6):
                start = base + i * 4 + 1
                end = base + (i + 1) * 4 + 1
                clusters.append(list(range(start, end)))
        return clusters

    if n_clusters == 365 * 12:
        # 2-hour clusters
        clusters = []
        for d in range(1, 366):
            base = (d - 1) * 24
            for i in range(12):
                start = base + i * 2 + 1
                end = base + (i + 1) * 2 + 1
                clusters.append(list(range(start, end)))
        return clusters

    raise ValueError(f"Unsupported number of clusters: {n_clusters}")