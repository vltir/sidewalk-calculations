import numpy as np
import matplotlib.pyplot as plt


def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-9 else v


def get_intersection(p1, u1, p2, u2):
    """Berechnet den Schnittpunkt zweier Geraden: p1 + t*u1 und p2 + s*u2"""
    # Matrix [u1, -u2]
    matrix = np.array([u1, -u2]).T
    det = np.linalg.det(matrix)

    if abs(det) < 0.1:  # Dein bewährter Schwellwert
        dot = np.dot(u1, u2)
        # Wenn parallel, nimm den Mittelwert der Versatzpunkte (Lot-Fallback)
        # Wir müssen hier prüfen, ob sie in die gleiche oder entgegengesetzte Richtung zeigen
        return (p1 + p2) / 2.0 if dot > 0 else (p1 + p2) / 2.0

    t = np.linalg.solve(matrix, p2 - p1)[0]
    return p1 + t * u1


def calculate_n_way_intersection(A, points, widths):
    # 1. Daten strukturieren und nach Winkel sortieren
    roads = []
    for p, w in zip(points, widths):
        vec = p - A
        angle = np.arctan2(vec[1], vec[0])
        roads.append({'unit': normalize(vec), 'width': w, 'angle': angle, 'target': p})

    # Sortierung gegen den Uhrzeigersinn
    roads.sort(key=lambda x: x['angle'])

    corners = []
    n = len(roads)

    for i in range(n):
        r1 = roads[i]
        r2 = roads[(i + 1) % n]  # Partner (wrap around)

        # r1: linker Bordstein (Normalen-Rotation: -y, x)
        n1 = np.array([-r1['unit'][1], r1['unit'][0]])
        p1 = A + (r1['width'] / 2.0) * n1

        # r2: rechter Bordstein (Normalen-Rotation: y, -x)
        n2 = np.array([r2['unit'][1], -r2['unit'][0]])
        p2 = A + (r2['width'] / 2.0) * n2

        # Schnittpunkt der zwei Kanten
        corner = get_intersection(p1, r1['unit'], p2, r2['unit'])
        corners.append(corner)

    return roads, corners


# --- Test mit einer 4-Wege-Kreuzung ---
A = np.array([0, 0])
pts = [
    np.array([10, 1]),  # Ost-ish
    np.array([-1, 10]),  # Nord-ish
    np.array([-12, -2]),  # West-ish
    np.array([2, -8])  # Süd-ish
]
wds = [4.0, 3.0, 5.0, 4.0]  # Unterschiedliche Breiten

sorted_roads, corner_pts = calculate_n_way_intersection(A, pts, wds)

# --- Visualisierung ---
plt.figure(figsize=(8, 8))
plt.scatter(*A, color='black', label='Zentrum A')

n = len(sorted_roads)
for i in range(n):
    plt.plot([A[0], sorted_roads[i]['target'][0]], [A[1], sorted_roads[i]['target'][1]], 'k--', alpha=0.3)
    vec = normalize(sorted_roads[i]['unit'])
    for j in [-1, 0]:
        c = corner_pts[(i+j)%n]
        e = c + 8 * vec
        plt.plot([c[0], e[0]], [c[1], e[1]], 'r', linewidth=2)

# Eckpunkte zeichnen
corners_plot = np.array(corner_pts + [corner_pts[0]])  # schließen für Plot
plt.plot(corners_plot[:, 0], corners_plot[:, 1], 'r-o', label='Bordstein-Kanten')

plt.axis('equal')
plt.grid(True)
plt.legend()
plt.title(f"{len(pts)}-Wege Kreuzung mit variablen Breiten")
plt.show()