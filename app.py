
from flask import Flask , render_template , request , redirect , url_for
from Kc import kkc
app = Flask(__name__)

_code = ""
region = {
        "Sud":2500,
        "Est":2000,
        "Nord et West":1700
}
import pandas as pd
import numpy as np
data = pd.read_excel('data_plante.xlsx')
#la formule generale pour calculer la dose d'eau
def ETM(list_Kc,rg_value):
        etp = rg_value*0.0018
        dose = [round(x*etp) for x in list_Kc['value']]
        step = list_Kc['step']
        result = []
        for i in range(0,len(dose)):
                result.append([step[i] , dose[i]])
        return dict(result)


@app.route("/index", methods=["GET","POST"])
def main():
                return render_template('index.html')


@app.route("/analyse", methods=["POST"])
def analyse():
        if(request.method == "POST"):
                import pandas as pd
                import numpy as np
                #importer notre dataset
                global data

                data['N'] =  data.N.astype(float)
                data['P'] =  data.P.astype(float)
                data['K'] =  data.K.astype(float)
                data['TEMPERATURE'] =  data.TEMPERATURE.astype(float)
                X =  data.drop("CLASS",axis=1)
                y =  data.CLASS

                # faire le training
                from sklearn.neighbors import KNeighborsClassifier
                clf = KNeighborsClassifier(n_neighbors=3)
                clf.fit(X,y)
                print(request.form.get('Potassium'))
                # recuperation des entres d'utilisateur

                potassium = request.form.get('Potassium')
                phosphorous = request.form.get('Phosphorous')
                nitrogen = request.form.get('Nitrogen')
                pH = str(request.form.get('pH')).replace(',' , '.')
                rg = request.form.get('Rg')
                rg=region[rg]
                print(rg)


                temperature = request.form.get('Temperature')

                resultats = []
                columns = ['N','P','K','pH','TEMPERATURE']
                values = np.array([ nitrogen ,phosphorous ,potassium ,   pH , temperature])
                pred = pd.DataFrame(values.reshape(-1, len(values)),columns=columns)
                        # print(pred.dtype)
                print(pred)
                # detecter les 3 voisins
                prediction = clf.predict(pred)
                print(prediction)

                plante =kkc[prediction[0]-1]
                dose_eau = ETM(plante , float(rg))

                resultats.append(dose_eau)

                data =  data[ data['CLASS'] != prediction[0]]
                X =  data.drop("CLASS",axis=1)
                y =  data.CLASS
                clf = KNeighborsClassifier(n_neighbors=3)
                clf.fit(X,y)
                prediction1 = clf.predict(pred)
                print(prediction1)

                plante =kkc[prediction1[0]-1]
                dose_eau = ETM(plante , float(rg))

                resultats.append(dose_eau)

                data =  data[ data['CLASS'] != prediction1[0]]
                X =  data.drop("CLASS",axis=1)
                y =  data.CLASS
                clf = KNeighborsClassifier(n_neighbors=3)
                clf.fit(X,y)
                prediction2 = clf.predict(pred)
                print(prediction2)

                plante =kkc[prediction2[0]-1]
                dose_eau = ETM(plante , float(rg))

                resultats.append(dose_eau)

                p1 = prediction1[0]
                p2 = prediction2[0]
                p1 = p1 -1
                p2 = p2 -1
                # print()
                print(resultats)

                if(prediction == 7):
                        return render_template('crops.html' , crop="TOMATO" , crop1=prediction1[0] , crop2=prediction2[0] ,result=resultats )
                elif(prediction == 1):
                        return render_template('crops.html' , crop="GARLIC" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats )
                elif(prediction == 2):
                        return render_template('crops.html' , crop="ONION" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats )
                elif(prediction == 3):
                        return render_template('crops.html' , crop="ORANGE" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats)
                elif(prediction == 4):
                        return render_template('crops.html' , crop="PEAS" , crop1=prediction1[0] , crop2=prediction2[0] ,result=resultats)
                elif(prediction == 5):
                        return render_template('crops.html' , crop="POTATO" , crop1=prediction1[0] , crop2=prediction2[0] ,result=resultats)
                elif(prediction == 6):
                        return render_template('crops.html' , crop="RICE" , crop1=prediction1[0] , crop2=prediction2[0] ,result=resultats)
                elif(prediction == 8):
                        return render_template('crops.html' , crop="SUGARCANE" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats)
                elif(prediction == 9):
                        return render_template('crops.html' , crop="Carotte" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats)
                elif(prediction == 10):
                        return render_template('crops.html' , crop="Poivron" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats)
                elif(prediction == 11):
                        return render_template('crops.html' , crop="Poireaux" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats)
                elif(prediction == 12):
                        return render_template('crops.html' , crop="Betterave" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats)
                elif(prediction == 13):
                        return render_template('crops.html' , crop="Epinards" , crop1=prediction1[0] , crop2=prediction2[0],result=resultats)
                
                
                else:
                        return "no"

        # render_template('index.html')
        else:
                return render_template('index.html')






if (__name__ == "__main__"):
        app.run(debug=False)
