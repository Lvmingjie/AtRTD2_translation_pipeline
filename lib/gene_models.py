class Gene(object):
    def __init__(self, name):
        assert name.startswith('AT')
        self.name = name
        self.transcript_dict = {}
        self.atg_list = []
        self.rep_atg = ''
        self.transposon = False
       
    def add_sense(self, sense):
        assert sense == '-' or sense == '+'
        self.sense = sense
        
    def get_atg_list(self):
        atg_list = [[], []]
        for transcript_ID in self.transcript_dict:
            transcript_model = self.transcript_dict[transcript_ID]
            atg = transcript_model.get_atg()
            atg_list[0].append(transcript_ID)
            atg_list[1].append(atg)
        return atg_list
    
    def get_orf_lengths(self):
        orf_lengths = [[], []]
        for transcript_ID in self.transcript_dict:
            transcript_model = self.transcript_dict[transcript_ID]
            orf_length = transcript_model.get_orf_length()
            orf_lengths[0].append(transcript_ID)
            orf_lengths[1].append(orf_length)
        return orf_lengths
   
    def mRNA_lengths(self):
        mRNA_lengths = [[], []]
        for transcript_ID in self.transcript_dict:
            transcript_model = self.transcript_dict[transcript_ID]
            mRNA = transcript_model.mRNA
            if mRNA == None: # non-coding transcript model at a coding locus
                continue
            mRNA_length = 1 + int(mRNA[1]) - int(mRNA[0])
            mRNA_lengths[0].append(transcript_ID)
            mRNA_lengths[1].append(mRNA_length)
        return mRNA_lengths
              
    def add_bounds(self, bounds):
        self.boundaries = bounds
        return


class Transcript(object):
    def __init__(self, name):
        self.name = name
        self.sense = None
        self.mRNA = None
        self.exon_list = []
        self.cds_list = []
        self.orf = []
        self.seq = ''
        self.cds_trim_seq = ''
    def add_exon(self, exon):
        if exon not in self.exon_list:	
            self.exon_list.append(exon)
            self.exon_list.sort()
        else: pass
    def add_CDS(self, cds):
        self.cds_list.append(cds)
        self.cds_list.sort()
        self.orf = [self.cds_list[0][0], self.cds_list[-1][1]]
    def add_ORF(self, ORF):
        self.orf = ORF     
    def get_atg(self):
        if self.sense == '+' and self.cds_list != []:
            return self.cds_list[0][0]
        elif self.sense == '-' and self.cds_list != []:
            return self.cds_list[-1][1]
        else: return # There is one transcript, AT1G77080.1, that has no annotated CDS
            
    def get_orf_length(self):
        if self.cds_list != []:
            return 1 + self.cds_list[-1][1] - self.cds_list[0][0]
        else: return
