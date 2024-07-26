from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # Récupération des données du formulaire
    sex = request.form.get('sex')
    weight = float(request.form.get('weight'))
    body_type = request.form.get('body_type')
    intensity = int(request.form.get('intensity'))
    duration_minutes = int(request.form.get('duration_minutes'))
    activity_type = request.form.get('activity_type')
    age = int(request.form.get('age'))

    # Matrice des apports en glucides (g/h) selon la durée et l'intensité de l'effort
    carb_matrix = {
        (0, 60): [0, 0, 0, 0, 0],
        (60, 120): [30, 40, 50, 60, 70],
        (120, 150): [40, 50, 60, 70, 80],
        (150, 180): [50, 60, 70, 80, 90],
        (180, float('inf')): [60, 70, 80, 90, 100]
    }

    # Coefficients spécifiques
    body_type_coeff = {'mince': 1.0, 'musclé': 1.1, 'embonpoint': 0.9}
    sex_coeff = {'homme': 1.0, 'femme': 0.9}
    activity_type_coeff = {
        'course': 1.0, 'cyclisme': 0.95, 'natation': 1.1, 
        'ski_de_fond': 1.1, 'trail': 1.2, 'vtt': 1.3, 'triathlon': 1.0
    }
    age_coeff = 1.0
    if age < 20:
        age_coeff = 1.1
    elif age >= 40:
        age_coeff = 0.9

    # Déterminer l'apport en glucides de base en fonction de la durée et de l'intensité
    base_carb_intake = 0
    for (min_duration, max_duration), carb_values in carb_matrix.items():
        if min_duration < duration_minutes <= max_duration:
            base_carb_intake = carb_values[intensity - 1]
            break

    # Ajuster en fonction du poids
    adjusted_carb_intake = base_carb_intake * (weight / 70)

    # Déterminer le ratio solide/liquide en fonction de la durée de l'effort
    if duration_minutes <= 60:
        liquid_carb_ratio = 0.8  # Principalement liquide
    elif 60 < duration_minutes <= 150:
        liquid_carb_ratio = 0.6  # 60% liquide, 40% solide
    else:
        liquid_carb_ratio = 0.7  # 70% liquide, 30% solide

    # Calcul des quantités de glucides liquide et solide
    liquid_carbs = adjusted_carb_intake * liquid_carb_ratio
    solid_carbs = adjusted_carb_intake * (1 - liquid_carb_ratio)

    # Total des glucides recommandés pour toute la session
    total_carbs_recommended = adjusted_carb_intake * (duration_minutes / 60)

    # Ratio Glucose:Fructose 2:1 pour les apports > 60 g/h
    glucose = adjusted_carb_intake * 2 / 3
    fructose = adjusted_carb_intake / 3

    # Arrondir les valeurs
    adjusted_carb_intake = round(adjusted_carb_intake)
    glucose = round(glucose)
    fructose = round(fructose)
    liquid_carbs = round(liquid_carbs)
    solid_carbs = round(solid_carbs)
    total_carbs_recommended = round(total_carbs_recommended)

    return render_template('result.html', total_carbs=adjusted_carb_intake, glucose=glucose, fructose=fructose,
                           liquid_carbs=liquid_carbs, solid_carbs=solid_carbs, total_carbs_recommended=total_carbs_recommended,
                           body_type=body_type, sex=sex, intensity=intensity, duration_minutes=duration_minutes,
                           activity_type=activity_type, age=age, base_carb_intake=base_carb_intake,
                           body_type_coeff=body_type_coeff, sex_coeff=sex_coeff, activity_type_coeff=activity_type_coeff,
                           age_coeff=age_coeff)

if __name__ == '__main__':
    app.run(debug=True)
