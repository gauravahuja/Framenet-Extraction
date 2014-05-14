
import java.util.Collection;
import java.util.List;
import java.io.StringReader;

import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;

import java.io.BufferedReader;
import java.io.FileReader;


class ParseSentences {

  public static void main(String[] args) {
    
    if (args.length == 1) {
      LexicalizedParser lp = LexicalizedParser.loadModel("edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz");
      demoDP(lp, args[0]);
    } else {
      System.out.println("Usage java ParseSentences sentences.txt");
    }
  }

  /**
   * demoDP demonstrates turning a file into tokens and then parse
   * trees.  Note that the trees are printed by calling pennPrint on
   * the Tree object.  It is also possible to pass a PrintWriter to
   * pennPrint if you want to capture the output.
   */
  public static void demoDP(LexicalizedParser lp, String filename) {
    // This option shows loading, sentence-segmenting and tokenizing
    // a file using DocumentPreprocessor.
    TreebankLanguagePack tlp = new PennTreebankLanguagePack();
    GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();
        
    int i = 0;
    BufferedReader br = null;
    String sentence = "";
    
    try{
        br = new BufferedReader(new FileReader(filename));
        sentence = br.readLine();
    }
    catch(Exception e){
        System.out.println("Error: Opening file "+filename);
    }
    
    while(sentence != null){
        i = i+1;

        TokenizerFactory<CoreLabel> tokenizerFactory = PTBTokenizer.factory(new CoreLabelTokenFactory(), "");
        Tokenizer<CoreLabel> tok = tokenizerFactory.getTokenizer(new StringReader(sentence));
        List<CoreLabel> rawWords = tok.tokenize();
        Tree parse = lp.apply(rawWords);

        GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
        List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
        //System.out.println(tdl);
        //System.out.println();


        System.out.println("Sentence#"+i);
        TreePrint tp = new TreePrint("penn,typedDependenciesCollapsed", "lexicalize", tlp);
        tp.printTree(parse);

        try{
            sentence = br.readLine();
        }
        catch(Exception e){
            System.out.println("Error readling line");
        }
    }
    //br.close();
  }

  private ParseSentences() {} // static methods only

}
