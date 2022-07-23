def buildTerm(term):
    term = term.upper()
    if term == 'AND':
        return '+'
    elif term == 'OR':
        return ' '
    elif term == 'NOT':
        return '-'
    else:
        return ''

def buildQuery(search):
    zQuery = '+'
    
    for term in search.split():
        bTerm = buildTerm(term)
        if bTerm == '':
            zQuery += term + ' '
        else:
            zQuery += bTerm
    
    return zQuery
  
   
print(buildQuery('sameer and sana'))