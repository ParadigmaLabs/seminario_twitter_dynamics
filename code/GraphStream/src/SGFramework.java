import java.io.FileInputStream;
import java.io.IOException;
import java.nio.CharBuffer;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.Charset;
import java.nio.charset.CharsetDecoder;
import java.util.Scanner;

import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.Edge;
import org.graphstream.graph.implementations.DefaultGraph;


/**
 * 
 * @author Roberto Maestre Martinez rmaestre@paradigmatecnologico.com
 * @author F. Javier Alba fjalba@paradigmatecnologico.com
 * 
 * Paradigma labs 2012. http://labs.paradigmatecnologico.com/
 *
 */
public class SGFramework {
	
	
	/**
	 * @param g Global graph
	 * @param nodeLabel Node label
	 * @param size Node size
	 * @param url Url to represent node with a image
	 */
	public static void addNode(Graph g, String nodeLabel, double size, String url){
		if (g.getNode(nodeLabel) == null){
			if (size < 0.0)
				size = 1.0;
			g.addNode(nodeLabel);
			Node n = g.getNode(nodeLabel);
			size = size * 2.0;
			String shape = "rounded-box";
			if (size > 20.0){
				shape = "cross";
			} 
			n.setAttribute("label",nodeLabel);
			
			//Ejemplo 1
			//n.addAttribute("ui.style" , String.format("size: %spx, %spx; fill-color: #3d5689; shape: %s; text-size: %s; stroke-mode: plain; stroke-color: yellow; text-color:white;",20, 20, "circle", size));
			
			//Ejemplo 2
			n.addAttribute("ui.style" , String.format("size: %spx, %spx; fill-color: #3d5689; shape: %s; text-size: %s; stroke-mode: plain; stroke-color: yellow; text-color:white;",size, size, shape, size));
		
			//Ejemplo 3
			//n.addAttribute("ui.style" , String.format("size: %spx, %spx; fill-color: #3d5689; shape: %s; text-size: %s; stroke-mode: plain; stroke-color: yellow; text-color:white; fill-mode: image-scaled; fill-image: url('%s');",size, size, "circle", size, url));
		}
	}
	
	
	/**
	 * @param g Global graph
	 * @param nodeLabel
	 */
	public static void removeNode(Graph g, String nodeLabel){
		if (g.getNode(nodeLabel) != null)
			g.removeNode(nodeLabel);
	}
	
	/**
	 * @param g Global graph
	 * @param nodeLabel Node label
	 * @param size Node size
	 */
	public static void changeNode(Graph g, String nodeLabel, double size){
		if (g.getNode(nodeLabel) != null){
			if (size < 0.0)
				size = 2.0;
			Node n = g.getNode(nodeLabel);
			String shape = "rounded-box";
			if (size > 20.0){
				shape = "cross";
			} 
			n.addAttribute("ui.stylesheet" , String.format("size: %spx, %spx;shape: %s; text-size: %s; ", size, size, shape, size/2));
		}
	}
	
	/**
	 * @param g Global graph
	 * @param from Node from
	 * @param to Node to
	 * @param weight Weight of edge
	 */
	public static void addEdge(Graph g, String from, String to, double weight){
		if (g.getNode(from) != null && g.getNode(to) != null && g.getEdge(from+to) == null && g.getEdge(to+from) == null){
			g.addEdge(from+to, from, to, true);
			Edge e = g.getEdge(from+to);
			if (weight < 0.0)
				weight = 1.0;
		    e.addAttribute("ui.style" , String.format("fill-color: #3d5689; size: %s;", weight));
		}
	}
	
	/**
	 * @param g Global graph
	 * @param from Node from
	 * @param to Node edge
	 */
	public static void removeEdge(Graph g, String from, String to){
		g.removeEdge(from, to);
	}
	
	public static void main(String args[]) throws IOException, InterruptedException {
	    
		System.setProperty("gs.ui.renderer", "org.graphstream.ui.j2dviewer.J2DGraphRenderer");
		System.setProperty("sun.java2d.opengl", "True");
		
		// Create graph
		Graph g = new DefaultGraph("g");
		// Display in real time console
		g.display(true);
		// Set some quality params
		g.addAttribute("ui.antialias");
		g.addAttribute("ui.quality");
		g.addAttribute("ui.stylesheet", "graph { fill-color: black; }");
		
		String file = "/tmp/hastag_coocurrence.tsv";
		
		FileChannel fc = new FileInputStream(file).getChannel();
		   
	    MappedByteBuffer byteBuffer = fc.map(FileChannel.MapMode.READ_ONLY, 0, fc.size());
	    Charset charset = Charset.forName("ISO-8859-1");
	    CharsetDecoder decoder = charset.newDecoder();
	    CharBuffer charBuffer = decoder.decode(byteBuffer);
	   
	    // Read file line by line
	    Scanner sc = new Scanner(charBuffer).useDelimiter("\n");
	   
	    while (sc.hasNext()) {
	        String line = sc.next();     
	        String[] chunks = line.split("\t");
	        if (chunks.length == 7) {
	        		addNode(g, chunks[0], Math.log( Double.parseDouble(chunks[1])) + 2, chunks[2]+3.0);	 
	        		addNode(g, chunks[3], Math.log( Double.parseDouble(chunks[4])) + 2, chunks[5]+3.0);	 
	        		addEdge(g, chunks[0], chunks[3], Math.log((Double.parseDouble(chunks[6]))));
	        }
	    }
	    fc.close();
	}
	   
}
