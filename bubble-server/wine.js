now=(new Date()).getTime()
data=[]
for (var ff=0;ff<1000;ff++) {
data.push({time:now+=6000,flavour:"raspberry"})
if (ff/20==Math.floor(ff/20)) now+=20000
}
data
bins={}

data.forEach(function(e){
    if (!bins) bins={}
    if (!bins[e.flavour]) bins[e.flavour]=[]
    bins[e.flavour].push(e.time);
})


bins["raspberry"].sort()
bins["raspberry"]=bins["raspberry"].sort()

bins["raspberry"]=bins["raspberry"].map(function(e,i,d) { return {time:e, diff:e-d[i-1]} })

perminute={}

Array.prototype.average=function() {
    var total=0;
    var count=0;
    this.forEach(function(v) { if (!isNaN(v)) { count++; total+=v } })
    return total/count
}

bins["raspberry"].forEach(function(e) {
    
    if (!perminute) perminute={}
    if (!perminute["raspberry"]) perminute["raspberry"]=[]
    min=Math.floor(e.time/60000)
    if (!perminute["raspberry"][min]) perminute["raspberry"][min]=[]
    perminute["raspberry"][min].push(e.diff)
        
    
})


