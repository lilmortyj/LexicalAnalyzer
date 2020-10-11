__author__ = 'JYH' 


import sys


#词法分析器中的运算符
Operation=['+', '-', '*', '/', '=', '#', '<', '<=', '>', '>=', ':=']
#词法分析器中的界符
Delimiter=['(', ')', ',', ';', '.']
#词法分析器中的保留字
KeyWord=['const', 'var', 'procedure', 'begin', 'end', 'odd', 'if', 'then', 'call', 'while', 'do', 'read', 'write']
#类别词典
sym={
    0:'nul',
    1:['constsym', 'varsym', 'procsym', 'beginsym', 'endsym', 'oddsym', 'ifsym', 'thensym', 'callsym', 'whilesym', 'dosym', 'readsym', 'writesym'],
    2:'ident',
    3:'number',
    4:['plus', 'minus', 'times', 'slash', 'becomes', 'neq', 'lss', 'leq', 'gtr', 'geq' ,'becomes'],
    5:['lparen','rparen','comma','semicolon','period']
}
#多行左注释标志
LeftNoteFlag=0 
#多行右注释标志
RightNoteFlag=0


class LexicalAnalyzer(): 
    '''词法分析器'''
    def IsLetter(self,Char): 
        '''判断该字符是否为字母''' 
        if((Char>='a' and Char<='z') or( Char>='A' and Char<='Z')): 
            return True 
        else: 
            return False 
  
    def IsDigit(self,Char): 
        '''判断该字符是否为数字''' 
        if(Char<='9' and Char>='0'): 
            return True 
        else: 
            return False 
  
    def IsSpace(self,Char): 
        '''判断是否为空白''' 
        if(Char==' '): 
            return True 
        else: 
            return False
    
    def RemoveSpace(self,List): 
        '''去除每一行代码的空白符号'''                                                                                                    #清除字符串中前后的空格 
        indexInList=0 
        for String in List:
            #str.strip() 移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
            List[indexInList]=String.strip() 
            indexInList+=1 
        return List 
  
    def IsNote(self,String): 
        '''判断该行代码是否存在注释'''                                                                                                     #判断注释类型 
        global LeftNoteFlag 
        global RightNoteFlag 
        index=0
        for Char in String: 
            if(index<len(String)): 
                #index始终比char大1 
                index+=1 
            if(Char=='/'): 
                if(String[index]=='/'): 
                    #存在注释符号 
                    return 2 
                elif(String[index]=='*'): 
                    if(LeftNoteFlag==0): 
                        LeftNoteFlag+=1 
                    #存在多行左注释符号 
                    return 1 
            elif(Char=='*'): 
                if(String[index]=='/'): 
                    if(RightNoteFlag==0): 
                        RightNoteFlag+=1 
                    #存在多行右注释符号 
                    return 3 
            #遍历结束，该行代码不存在注释 
            if(len(String)==index+1): 
                    return False 
  
    def DeleteNote(self,List):                                                                                                   #删除列表中的注释『'//'或者'/*   */'』 
        '''删除所有注释''' 
        #要删除的注释的列表 
        RemoveList=[]
        #左注释符号前最后一个位置
        LeftNoteNum1=0
        #代码行数
        indexInList=0
        global LeftNoteFlag 
        global RightNoteFlag 
        for String in List:  
            Flag=self.IsNote(String) 
            index=0 
            LeftNoteNum1=0 
            #如果该行存在注释 
            if(Flag): 
                for Char in String: 
                    if(index<len(String)-1): 
                        index+=1 
                	#存在多行左注释符号 
                    if(Flag==1): 
                        if(Char=='/' and String[index]=='*'): 
                            if(index!=1): 
                                #左注释前有字符
                                LeftNoteNum1=index-2 
                            else: 
                                #左注释符号开始的位置，=0，左注释符号前没有字符 
                                LeftNoteNuml=0
                        if(Char=='*' and String[index]=='/'): 
                            if(index!=len(String)-1): 
                                #找到右注释，且不在结尾处，则删除中间的注释 
                                String=String[0:LeftNoteNum1+1]+String[index+1:] 
                            else: 
                                #找到右注释，且在结尾处，则删除后面的注释 
                                String=String[0:LeftNoteNum1+1] 
                            #左注释标志置0 
                            LeftNoteFlag=0 
                            break 
                        #字符串结束，且没有右注释符号，且该行存在左注释 
                        if(index+1==len(String) and RightNoteFlag==0 and LeftNoteFlag==1 ):                                                  
                            if(LeftNoteNum1==0): 
                        	    #左注释符号在开头，将该行代码加入待删除的列表 
                                RemoveList.append(String) 
                            else: 
                                #直接删除该行代码后部分的注释 
                                String=String[0:LeftNoteNum1+1]                                           
                            break
                    elif(Flag==2): 
                        #存在注释符号 
                        if(Char=='/' and String[index]=='/'): 
                            #直接去掉该注释 
                            String=String[0:index-1] 
                            break 
                    elif(Flag==3): 
                        #存在多行右注释符号 
                        if(Char=='*' and String[index]=='/'): 
                            #存在左注释，且右注释不在该行代码结尾处 
                            if(LeftNoteFlag!=0 and index!=len(String)-1): 
                                #删除该行前半部分的右注释 
                                String=String[index+1:] 
                            #不存在左注释，应该报错 
                            elif LeftNoteFlag==0: 
                                raise Exception("语法错误，缺少多行左注释符号")
                            #存在右注释，且右注释在该行代码的结尾处 
                            elif(LeftNoteFlag!=0 and index+1==len(String)): 
                                #将该行添加到预删除掉列表中 
                                RemoveList.append(String) 
                            #将左右注释标志置0 
                            RightNoteFlag=0
                            LeftNoteFlag=0
                            break 
            else: 
            #若该行不存在注释
            	#若存在左注释，且不存在右注释 
                if(LeftNoteFlag!=0 and RightNoteFlag==0): 
                    #将该行添加进删除列表
                    RemoveList.append(String) 
                #若同时存在左注释和右注释 
                elif(LeftNoteFlag!=0 and RightNoteFlag!=0): 
                    #应该报错 
                    raise Exception("没有成功删除注释")
                else: 
                    pass 
 
            #更新代码列表 
            List[indexInList]=String 
            if(indexInList<len(List)-1): 
                indexInList+=1 
        #删除多行注释 
        for ListString in RemoveList: 
            List.remove(ListString) 
        return List 
  
    def Tokenizer(self,List): 
        '''分词器''' 
        #结果列表 
        ResultList=[] 
        for String in List: 
            Letter='' 
            Digit='' 
            letter='' 
            index=0 
            for Char in String: 
                if(index<len(String)-1): 
                    index+=1 
                #char是字母 
                if(self.IsLetter(Char)): 
                    #char的下一位是字母或数字 
                    if(self.IsLetter(String[index]) or self.IsDigit(String[index])): 
                        Letter+=Char 
                    #char的下一位是空白、分界符或运算符 
                    elif(self.IsSpace(String[index]) or (String[index] in Delimiter) or (String[index] in Operation) or (String[index:index+2] in Operation)): 
                        Letter+=Char 
                        #将单词加进结果列表，清空 
                        ResultList.append(Letter) 
                        Letter=''
                    else:
                        raise Exception("无法识别该符号")
                    if Char==String[-1]:
                        #以字母结尾，将单词加进结果列表，清空
                        ResultList.append(Letter) 
                        Letter=''
                else: 
                    #char是数字
                    if(self.IsDigit(Char)): 
                        #char的下一位是数字
                        if self.IsDigit(String[index]): 
                            Digit+=Char
                        #char的下一位是字母
                        elif self.IsLetter(String[index]):
                            raise Exception("非法标识符：标识符只能以字母开头")
                        #char的下一位是空白、分界符或运算符
                        elif (self.IsSpace(String[index]) or (String[index] in Delimiter) or (String[index] in Operation) or (String[index:index+2] in Operation)): 
                            Digit+=Char
                            #将数字加进结果列表，清空
                            ResultList.append(Digit)
                            Digit=''
                        else:
                            raise Exception("无法识别该符号")
                        if Char==String[-1]:
                            #以数字结尾，将数字加进结果列表，清空
                            ResultList.append(Letter) 
                            Digit=''
                    else:
                        #char是界符
                        if(Char in Delimiter):
                            ResultList.append(Char)
                        else:
                            #char是运算符
                            if(Char in Operation or Char == ':'):
                                if String[index-2]!=':' and String[index-2]!='<' and String[index-2]!='>':
                                    letter+=Char
                                if(String[index] in Operation):
                                    letter+=String[index]
                                    ResultList.append(letter)
                                    letter=''
                                else:
                                    ResultList.append(letter)
                                    letter=''
                            else:
                                #char是空白
                                if(self.IsSpace(Char)):
                                    pass
                                else:
                                    raise Exception("无法识别该符号")
        return ResultList
         
    def JudgeAndOutput(self,List): 
        '''种类判断和结果输出''' 
        #下一个单词的索引
        indexInList=0 
        for String in List: 
            if(indexInList<len(String)-1): 
                indexInList+=1
            #该单词只由1个字符构成
            if(len(String)==1):
                #分界符
                if(String in Delimiter):
                    print('<'+sym[5][Delimiter.index(String)]+','+String+'>')
                #运算符
                elif(String in Operation):
                    print('<'+sym[4][Operation.index(String)]+','+String+'>')
                else:
                    #数字
                    if(String.isdigit()): 
                        print('<'+sym[3]+','+String+'>')
                    #str.isalnum() 如果string至少有一个字符并且所有字符都是字母或数字则返回 True,否则返回 False
                    #标识符
                    elif(String.isalnum()): 
                        print('<'+sym[2]+','+String+'>')
            #该单词由多个字符构成
            else:
                #保留字
                if(String in KeyWord): 
                    print('<'+sym[1][KeyWord.index(String)]+','+String+'>')
                #运算符
                elif(String in Operation): 
                    print('<'+sym[4][Operation.index(String)]+','+String+'>')
                else:
                    #数字
                    if(String.isdigit()): 
                        print('<'+sym[3]+','+String+'>')
                    #标识符
                    elif(String.isalnum()): 
                        print('<'+sym[2]+','+String+'>')


def main():
    #创建词法分析器实例
    LA=LexicalAnalyzer() 
    SourceCode=[]
    Filepath = 'sourcecode.pas'#源代码文件路径
    with open(Filepath,'r',encoding='utf-8-sig') as f:
        for line in f:
            line=line.replace('\n','')
            SourceCode.append(line)
    sys.stdout = open('output.txt', mode='w', encoding='utf-8')#将输出写到文件中
    SourceCode=LA.DeleteNote(SourceCode)#删除注释
    SourceCode=LA.RemoveSpace(SourceCode)#删除空白
    SourceCode=LA.Tokenizer(SourceCode)#分词
    LA.JudgeAndOutput(SourceCode)#判断种类，输出结果

if __name__ == "__main__": 
    main()