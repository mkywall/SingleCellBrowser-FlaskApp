#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:20:28 2019

@author: morgan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:42:12 2019

@author: morgan
"""

# have to run this from within the venv environment
# activate this environment with . venv/bin/activate in 
# the /Users/morgan/myproject folder
from flask import Flask
from flask_heroku import Heroku
from flask import render_template
from flask import url_for, redirect, request, send_file
from flask_basicauth import BasicAuth
from passlib.hash import pbkdf2_sha256
from flask_sqlalchemy import SQLAlchemy
#from flask_images import Images
from werkzeug.contrib.cache import SimpleCache
#from sqlalchemy import create_engine, MetaData, Table
import seaborn as sns
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
matplotlib.use('Agg')
from pylab import savefig
#from models import *
import os
import base64
#from ggplot import *


app = Flask(__name__)

# configuration
app.config['BASIC_AUTH_USERNAME'] = 'kipnis'
app.config['BASIC_AUTH_PASSWORD'] = 'kipnis'
app.config['BASIC_AUTH_FORCE'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# random stuff
db = SQLAlchemy(app)
heroku = Heroku(app)
cache = SimpleCache()
#app.secret_key = 'coffee'
#images = Images(app)

# some security
basic_auth = BasicAuth(app)
myhash1 = pbkdf2_sha256.hash("kipnis")
myhash2 = pbkdf2_sha256.hash("kipnis")

# set up the database class
class Data(db.Model):
    __tablename__ = "alldata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    condition = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text())
    
class AData(db.Model):
    __tablename__ = "adata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text()) 
class BData(db.Model):
    __tablename__ = "bdata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text()) 
class CData(db.Model):
    __tablename__ = "cdata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text()) 
class DData(db.Model):
    __tablename__ = "ddata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text()) 
class EData(db.Model):
    __tablename__ = "edata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text()) 
class FData(db.Model):
    __tablename__ = "fdata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text()) 
class HData(db.Model):
    __tablename__ = "hdata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text()) 
class IData(db.Model):
    __tablename__ = "idata"
    cellnames = db.Column(db.Text(), primary_key=True)
    variable = db.Column(db.Text())
    value = db.Column(db.Float())
    sample = db.Column(db.Text())
    cluster = db.Column(db.Text())
    tsne1 = db.Column(db.Float())
    tsne2 = db.Column(db.Float())
    dataset = db.Column(db.Text())  

@app.route('/',)
@basic_auth.required
def index():
    return render_template('index.html')


@app.route('/loginpw', methods=['GET', 'POST'])
def loginpw():
    error = None
    if request.method == 'POST':
        if pbkdf2_sha256.verify(request.form['username'], myhash2) == False or pbkdf2_sha256.verify(request.form['password'], myhash1) == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            pname = request.form['yourname'] 
            return redirect(url_for('mainpage', name = pname))
    return render_template('loginpw.html', error=error)

    


@app.route('/main/<name>')
def mainpage(name):
    return render_template('mainpage.html', username=name)


@app.route('/result', methods=['GET', 'POST'])
def result():
    result = request.form
    
    # info needed to make query
    sn = result['Sample']
    genes = result['Genes']
    
    genelist = genes.split(",")
    genelist = [g.strip().lower().capitalize() for g in genelist]
    #genes = genes.strip().lower().capitalize()
    print(genelist)
    
    
    # query the data 
    dflist = []
    rmlist = []
    for gl in genelist:
        print(gl)
        dpoints = None
        if sn == "A":
            dpoints = AData.query.filter_by(variable=gl).all()
        elif sn == "B": 
            dpoints = BData.query.filter_by(variable=gl).all()
        elif sn == "C": 
            dpoints = CData.query.filter_by(variable=gl).all()
        elif sn == "D": 
            dpoints = DData.query.filter_by(variable=gl).all()
        elif sn == "E": 
            dpoints = EData.query.filter_by(variable=gl).all()
        elif sn == "F": 
            dpoints = FData.query.filter_by(variable=gl).all()
        elif sn == "H": 
            dpoints = HData.query.filter_by(variable=gl).all()
        elif sn == "I": 
            dpoints = IData.query.filter_by(variable=gl).all()
        else: 
            print("dataset doesn't exist")
            
        print("length of dpoints:" + str(len(dpoints)))
        if len(dpoints) > 0:
            print(dpoints[0:5])
            
            d = {"gene": [g.variable for g in dpoints], "exp": [g.value for g in dpoints], "sample": [g.sample for g in dpoints], 
                     "cluster": [g.cluster for g in dpoints],  "tsne1": [g.tsne1 for g in dpoints], 
                     "tsne2": [g.tsne2 for g in dpoints]}
            df = pd.DataFrame(data = d)
            if sn == "A":
                df.loc[:,"sample"] = pd.Categorical(df.loc[:, "sample"], categories = ["brain young", "brain old", "meninges young","meninges old"], ordered = True)
            elif sn == "B": 
                df.loc[:,"sample"] = pd.Categorical(df.loc[:, "sample"], categories = ["spleen pup", "spleen adult", "meninges pup", "meninges adult"], ordered = True)
            elif sn == "C": 
                df.loc[:,"sample"] = pd.Categorical(df.loc[:, "sample"], categories = ["young", "old"], ordered = True)
            elif sn == "D": 
                df.loc[:,"sample"] = pd.Categorical(df.loc[:, "sample"], categories = ["blood", "diaphragm", "meninges"], ordered = True)
            elif sn == "E": 
                df.loc[:,"sample"] = pd.Categorical(df.loc[:, "sample"], categories = ["wildtype", "5xfad", "5xfad Ablated"], ordered = True)
            elif sn == "F": 
                df.loc[:,"sample"] = pd.Categorical(df.loc[:, "sample"], categories = ["wildtype", "5xfad", "5xfad Ablated"], ordered = True)
            elif sn == "H": 
                df.loc[:,"sample"] = pd.Categorical(df.loc[:, "sample"], categories = ["wt nonengram", "wt engram", "scid nonengram", "scid engram"], ordered = True)
            elif sn == "I": 
                df.loc[:,"sample"] = pd.Categorical(df.loc[:, "sample"], categories = ["wt nonengram", "wt engram", "scid nonengram", "scid engram"], ordered = True)
                
            dflist.append(df)
            print(df.iloc[0:5, 0:5])
        elif len(dpoints) == 0:
            rmlist.append(gl)
            
    fulldf = pd.concat(dflist)
    rev_genelist = set(genelist) - set(rmlist)
    #print(fulldf.iloc[0:5, 0:5])
    cache.set('my-fulldf', fulldf, timeout=10 * 60)
    cache.set('my-genelist', rev_genelist, timeout = 10*60)
    return redirect(url_for('chooseplots1'))
    

@app.route('/chooseplots1')
def chooseplots1():
    genelist = cache.get("my-genelist")
    return render_template('chooseplots.html', genelist = genelist)



@app.route('/chooseplots', methods=['GET', 'POST'])
def chooseplots():
        result = request.form
        plottype = None
        plottype = result['Plot']
        #print(plottype)
        gene = None
        gene = result['Gene']
        #print(gene)
        fulldf = None
        fulldf = cache.get("my-fulldf")
        #print(fulldf.iloc[0:5, 0:5])
        df = None
        #print(fulldf['gene'])
        df = fulldf.loc[fulldf["gene"] == gene, :]
    
    # make the plot
        if plottype == "violin": 
                img = None
                groupby= result['groupby']
                if groupby == "cluster":
                    df.loc[:,"cluster"] = pd.Categorical(df.loc[:, "cluster"], categories = [str(y) for y in range(1,max([int(x) for x in df.loc[:, "cluster"].tolist()]))], ordered = True)
                img = BytesIO()
                sns.violinplot(x = groupby, y = "exp", 
                      data = df, scale = "width", palette = "viridis", inner = "points")
                plt.savefig(img)
                plt.close()
                img.seek(0)
                #cache.set('vplot', img, timeout = 1*60)
                plot_url = base64.b64encode(img.getvalue())
                plot_url = plot_url.decode('utf8')
                print(plot_url)
                h = "600"
                w = "800"
                return render_template('showimage.html', plot_url=plot_url, gene = gene, width = w, height = h)
                #return send_file(img, mimetype='image/png')
                #return redirect(url_for('getimage', ptype = 'vplot', gene = gene))
            
        if plottype == "tsne": 
                img = None
                cmap = sns.cubehelix_palette(dark=.1, light=.8, as_cmap=True)
                sns.scatterplot(df.loc[:,"tsne1"],df.loc[:,"tsne2"], hue = df.loc[:,"exp"],
                            palette = cmap, s= 8, edgecolor= None)
                img = BytesIO()
                plt.savefig(img)
                plt.close()
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue())
                plot_url = plot_url.decode('utf8')
                print(plot_url)
                h = "600"
                w = "800"
                return render_template('showimage.html', plot_url=plot_url, gene = gene, width = w, height = h)
                #return send_file(img, mimetype='image/png')
        
        
        if plottype == "swarmplot": 
                img = None
                groupby= result['groupby']
                colorby = result['colorby']
                cmap = sns.cubehelix_palette(dark=.1, light=.8, as_cmap=True)
                
                sns.swarmplot(x=groupby, y="exp", hue=colorby,
                  palette='viridis', data=df)
            
                img = BytesIO()
                plt.savefig(img)
                plt.close()
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue())
                plot_url = plot_url.decode('utf8')
                print(plot_url)
                return render_template('showimage.html', plot_url=plot_url, gene = gene)
                #return send_file(img, mimetype='image/png')
            

        
#@app.route('/image')
#def images():
 #   return render_template("vln_res.html")


#@app.route('/getimage/<gene>/<ptype>')
#def getimage(ptype, gene):
#    gene = gene
#    img = cache.get(ptype)
#    return render_template("showimage.html", img = img, gene = gene)






if __name__ == '__main__':
    app.run(debug=True)

    
