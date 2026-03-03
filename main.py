import numpy as np
import matplotlib.pyplot as plt


def calculate_curb_corner(a, b, c, width_ab, width_ac, side="left"):
    # 1. Richtungsvektoren
    dir_ab = b - a
    dir_ac = c - a
    ab = dir_ab / np.linalg.norm(dir_ab)
    ac = dir_ac / np.linalg.norm(dir_ac)

    # 2. Normalenvektoren (90 Grad Drehung)
    # Links von A->B: (-y, x), Rechts von A->B: (y, -x)
    if side == "left":
        n_ab = np.array([ab[1], -ab[0]])
        n_ac = np.array([-ac[1], ac[0]])
    else:
        n_ab = np.array([-ab[1], ab[0]])
        n_ac = np.array([ac[1], -ac[0]])

    # 3. Hilfspunkte auf den Bordsteinkanten
    p_ab = a + .5 * width_ab * n_ab
    p_ac = a + .5 * width_ac * n_ac

    det = ab[0] * (-ac[1]) - (-ac[0] * ab[1])
    print(det)
    # 4. Determinante berechnen, um Parallelität zu prüfen
    if abs(det) < 1e-1:
        # --- SPEZIALFALL: PARALLEL ---
        dot = np.dot(ab, ac)
        print(dot)
        if dot > 0:
            p_ac = a - .5 * width_ac * n_ac
        # Wir nehmen den Mittelpunkt der beiden versetzten Punkte.
        # Das entspricht genau deinem Vorschlag: E steht im Lot zu A.
        print("Spezialfall: Straßen sind parallel. Berechne Lot-Punkt.")
        e = (p_ab + p_ac) / 2.0
        return e, p_ab, p_ac

    # 5. Schnittpunkt der zwei versetzten Geraden (LGS lösen)
    # Gleichung: p_ab + t*ab = p_ac + s*ac
    matrix = np.array([ab, -ac]).T
    rhs = p_ac - p_ab

    try:
        params = np.linalg.solve(matrix, rhs)
        t = params[0]
        e = p_ab + t * ab
        return e, p_ab, p_ac
    except np.linalg.LinAlgError:
        return None


# --- Setup Testdaten ---
A = np.array([0, 0])
B = np.array([10, 0])  # Straße 1 (leicht schräg)
C = np.array([10, 10]) # Straße 2
w_ab, w_ac = 4.0, 2.0  # Unterschiedliche Breiten

# Berechnung
result = calculate_curb_corner(A, B, C, w_ab, w_ac, side="right")
if result:
    E, Pab, Pac = result

    # --- Visualisierung ---
    plt.figure(figsize=(8, 8))

    # 1. Straßenmittellinien
    plt.plot([A[0], B[0]], [A[1], B[1]], 'gray', linestyle='--', label='Straßenmitte')
    plt.plot([A[0], C[0]], [A[1], C[1]], 'gray', linestyle='--')

    # 2. Bordsteinkanten (als Linien vom Eckpunkt weg)
    # Wir zeichnen sie einfach parallel zu den Mittellinien
    u_ab = (B - A) / np.linalg.norm(B - A)
    u_ac = (C - A) / np.linalg.norm(C - A)
    plt.plot([E[0], E[0] + u_ab[0] * 10], [E[1], E[1] + u_ab[1] * 10], 'r', linewidth=2, label='Bordstein')
    plt.plot([E[0], E[0] + u_ac[0] * 10], [E[1], E[1] + u_ac[1] * 10], 'r', linewidth=2)

    # 3. Punkte markieren
    plt.scatter([A[0], B[0], C[0]], [A[1], B[1], C[1]], c='blue')
    plt.annotate('A (Kreuzung)', A, textcoords="offset points", xytext=(0, 10), ha='center')

    plt.scatter([E[0]], [E[1]], c='red', s=100, zorder=5)
    plt.annotate('E (Eckpunkt)', E, textcoords="offset points", xytext=(10, -15), color='red', weight='bold')

    # Achsen-Einstellungen
    plt.axis('equal')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.title(f"Bordstein-Eckpunkt Berechnung\nStraßenbreiten: AB={w_ab}m, AC={w_ac}m")
    plt.show()