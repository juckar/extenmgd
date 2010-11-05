import java.security.PrivateKey;
import java.security.cert.Certificate;

import java.io.*;
import java.net.URL;
import java.net.URLDecoder;
import java.security.CodeSource;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.Provider;
import java.security.ProviderException;
import java.security.Security;
import java.security.UnrecoverableKeyException;
import java.security.cert.Certificate;
import java.security.cert.CertificateException;
import java.util.NoSuchElementException;
import java.util.ResourceBundle;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.Enumeration;

import sun.security.pkcs11.SunPKCS11;

import com.lowagie.text.pdf.PdfReader;
import com.lowagie.text.pdf.PdfSignatureAppearance;
import com.lowagie.text.pdf.PdfStamper;
import com.lowagie.text.pdf.BaseFont;
import com.lowagie.text.Rectangle;
import com.lowagie.text.Font;
// Nuevo 8/1/2009
import com.lowagie.text.Document;
import com.lowagie.text.pdf.PRAcroForm;
import com.lowagie.text.pdf.PdfCopy;
import com.lowagie.text.pdf.PdfImportedPage;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

/**
 * 
 * Basado en jPDFSign de Jan Peter Stotz 
 * http://private.sit.fraunhofer.de/~stotz/software/jpdfsign/
 * 
 */
public class FirmaDigital extends JPanel
                          implements ActionListener {

    private static PrivateKey privateKey;

    private static Certificate[] certificateChain;
    
    private static String OK = "ok";
    private static String OFF = "off";

    private JFrame controllingFrame; 
    private JPasswordField passwordField;
    private static boolean siFirmar = false;
    private static char[] clave;

    public static String jarPath;
    
    public static String tipoFD;
    public static String valorFD;
    public static String origenPDF;
    public static String destinoPDF;
    public static String motivo;
    public static String contacto;
    public static String ubicacion;
    public static boolean siRecuadro;
    public static String textoRecuadro;
    public static int filaRecuadro;
    public static int columnaRecuadro;
    public static int anchoRecuadro;
    public static int altoRecuadro;
    public static int pagina;
        

    public static void Firma() {
        

        try {
            if ( tipoFD.equals( "ALMACEN" ) ) {
                KeyStoreHelperMSCAPI k = new KeyStoreHelperMSCAPI( jarPath );
                k.loadProvider();
                k.openKeyStore();
                Enumeration<String> es = k.getAliases();
                k.loadAlias( valorFD );//, clave );
                certificateChain = k.getCertificateChain();
                privateKey = k.getPrivateKey();
            } else if  ( tipoFD.equals( "FICHERO" ) )
                readPrivateKeyFromPKCS12();
            else if  ( tipoFD.equals( "TARJETA" ) )
                readPrivateKeyFromPKCS11();
        
        } catch (Exception e) {
            LanzaError( "comprobando la clave" );
        }

        PdfReader reader = null;
        try {
            reader = new PdfReader(origenPDF);
        } catch (IOException e) {
            LanzaError( "abriendo el PDF a firmar : " + origenPDF );
        }
        
        // Nuevo 8/1/2009
        try {
            int n = reader.getNumberOfPages();
            Document document = new Document(reader.getPageSizeWithRotation(1));
            PdfCopy writer = new PdfCopy(document, new FileOutputStream("tmp.pdf"));
            document.open();
            PdfImportedPage page;
            for (int i = 0; i < n; ) {
                ++i;
                page = writer.getImportedPage(reader, i);
                writer.addPage(page);
            }
            PRAcroForm form = reader.getAcroForm();
            if (form != null)
                writer.copyAcroForm(reader);
            document.close();
        } catch (Exception e) {
            LanzaError( "creando el fichero temporal de trabajo" );
        }
        
        try {
            reader = new PdfReader("tmp.pdf");
        } catch (IOException e) {
            LanzaError( "creando el fichero temporal de trabajo" );
        }

        
        FileOutputStream fout = null;
        try {
            fout = new FileOutputStream(destinoPDF);
        } catch (FileNotFoundException e) {
            reader = null;
            LanzaError( "abriendo el PDF a crear : " + destinoPDF + ", probablemente lo tenga abierto con el lector de PDF" );
        }
        
        PdfStamper stp = null;
        try {
            stp = PdfStamper.createSignature(reader, fout, '\0');
            PdfSignatureAppearance sap = stp.getSignatureAppearance();
            sap.setCrypto(privateKey, certificateChain, null,
                    PdfSignatureAppearance.WINCER_SIGNED);
            if( siRecuadro ) {
                sap.setLayer2Text( textoRecuadro );
                BaseFont helvetica = BaseFont.createFont("Helvetica", BaseFont.CP1252, BaseFont.NOT_EMBEDDED);
                sap.setLayer2Font( new Font(helvetica, 8, Font.NORMAL ) );
                Rectangle r = new Rectangle(columnaRecuadro, filaRecuadro, columnaRecuadro + anchoRecuadro, filaRecuadro + altoRecuadro);
                sap.setVisibleSignature(r, pagina, null);
            }
            
            // Image signImg = Image.getInstance("stamp.gif");
            // sap.setImage(signImg);
            
            if( motivo != null ) 
                sap.setReason(motivo);
            if( contacto != null ) 
                sap.setContact(contacto);
            if( ubicacion != null )
                sap.setLocation(ubicacion);
            stp.close();
            
        } catch (Exception e) {
            LanzaError( "mientras se intentaba firmar el PDF (sap)" );
        }
    }

    private static void readPrivateKeyFromPKCS11() throws KeyStoreException {
        // Initialize PKCS#11 provider from config file
        String configFileName = jarPath + "pkcs11.cfg";

        Provider p = null;
        try {
            p = new SunPKCS11(configFileName);
            Security.addProvider(p);
        } catch (ProviderException e) {
            LanzaError( "no es correcto el fichero de configuración de la tarjeta" );
        }
        
        KeyStore ks = null;
        try {
            ks = KeyStore.getInstance("pkcs11", p);
            ks.load(null, clave );
        } catch (NoSuchAlgorithmException e) {
            LanzaError( "leyendo la tarjeta (n.1)" );
        } catch (CertificateException e) {
            LanzaError( "leyendo la tarjeta (n.2)" );
        } catch (IOException e) {
            LanzaError( "leyendo la tarjeta (n.3)" );
        }

        String alias = "";
        try {
            alias = (String) ks.aliases().nextElement();
            privateKey = (PrivateKey) ks.getKey(alias, clave);
        } catch (NoSuchElementException e) {
            LanzaError( "leyendo la clave de la tarjeta (n.1)" );
        } catch (NoSuchAlgorithmException e) {
            LanzaError( "leyendo la clave de la tarjeta (n.2)" );
        } catch (UnrecoverableKeyException e) {
            LanzaError( "leyendo la clave de la tarjeta (n.3)" );
        }
        certificateChain = ks.getCertificateChain(alias);
    }

    protected static void readPrivateKeyFromPKCS12()
            throws KeyStoreException {
        KeyStore ks = null;

        try {
            ks = KeyStore.getInstance("pkcs12");
            ks.load(new FileInputStream(valorFD), clave );
        } catch (NoSuchAlgorithmException e) {
            LanzaError( "leyendo el fichero con el certificado (n.1)" );
        } catch (CertificateException e) {
            LanzaError( "leyendo el fichero con el certificado (n.2)" );
        } catch (FileNotFoundException e) {
            LanzaError( "leyendo el fichero con el certificado (fichero no encontrado)" );
        } catch (IOException e) {
            LanzaError( "leyendo el fichero con el certificado (password errónea)" );
        }
        String alias = "";
        try {
            alias = (String) ks.aliases().nextElement();
            privateKey = (PrivateKey) ks.getKey(alias, clave );
        } catch (NoSuchElementException e) {
            LanzaError( "leyendo la clave del fichero con el certificado (n.1)" );
        } catch (NoSuchAlgorithmException e) {
            LanzaError( "leyendo la clave del fichero con el certificado (n.2)" );
        } catch (UnrecoverableKeyException e) {
            LanzaError( "leyendo la clave del fichero con el certificado (n.3)" );
        }
        certificateChain = ks.getCertificateChain(alias);
        
    }


    private static void leeParametros() {

        String         cLinea    = null;
        BufferedReader objBRdr    = null;
        FileReader     objFRdr    = null;
        int n;
        String cOrden = null;
        String cValor = null;
        
        tipoFD = null;
        valorFD = null;
        origenPDF = null;
        destinoPDF = null;
        motivo = null;
        contacto = null;
        ubicacion = null;
        siRecuadro = false;
        textoRecuadro = null;
        filaRecuadro = 0;
        columnaRecuadro = 0;
        anchoRecuadro = 0;
        altoRecuadro = 0;
        pagina = 1;
        try { 
            objFRdr = new FileReader(jarPath + "param.ini");
        
            if (objFRdr != null)
            {
                objBRdr = new BufferedReader(objFRdr);
                if (objBRdr != null)
                {
                    while (objBRdr.ready())
                    {
                        cLinea = null;
                        cLinea = objBRdr.readLine().trim();
                        if( cLinea.contains( "=" ) ) {
                            n = cLinea.indexOf( "=" );
                            cOrden = cLinea.substring( 0, n ).trim();
                            cValor = cLinea.substring( n+1 );

                            
                            if( cOrden.equals("TIPO") ) 
                                tipoFD = cValor;
                            else if( cOrden.equals( "VALOR" ) )
                                valorFD = cValor;
                            else if( cOrden.equals( "PAGINA" ) )
                                pagina = Integer.parseInt(cValor);
                            else if( cOrden.equals( "ORIGENPDF" ) )
                                origenPDF = cValor;
                            else if( cOrden.equals( "DESTINOPDF" ) )
                                destinoPDF = cValor;
                            else if( cOrden.equals( "MOTIVO" ) )
                                motivo = cValor;
                            else if( cOrden.equals( "CONTACTO" ) )
                                contacto = cValor;
                            else if( cOrden.equals( "UBICACION" ) )
                                ubicacion = cValor;
                            else if( cOrden.equals( "SIRECUADRO" ) )
                                siRecuadro = cValor.equals( "SI" );
                            else if( cOrden.equals( "TEXTORECUADRO" ) )
                                textoRecuadro = cValor.replaceAll( "·", "\n" );
                            else if( cOrden.equals( "FILARECUADRO" ) )
                                filaRecuadro = Integer.parseInt(cValor);
                            else if( cOrden.equals( "COLUMNARECUADRO" ) )
                                columnaRecuadro = Integer.parseInt(cValor);
                            else if( cOrden.equals( "ANCHORECUADRO" ) )
                                anchoRecuadro = Integer.parseInt(cValor);
                            else if( cOrden.equals( "ALTORECUADRO" ) )
                                altoRecuadro = Integer.parseInt(cValor);
                        }
                    }
                }
            }
            if (objBRdr != null)
            {
                objBRdr.close();
                objBRdr = null;
            }
            if (objFRdr != null)
            {
                objFRdr.close();
                objFRdr = null;
            }
        } catch (Exception e) {
            LanzaError( "leyendo el fichero de parámetros" );
        }
    }


    private static void LanzaError(String sError) {
        
        try {
            quitaHola();
            File f=new File( jarPath + "errorFD.err");
            FileWriter fw=new FileWriter(f);
            fw.write( sError );
            fw.close();
            System.exit(-1);
        } catch (Exception e) {
            System.exit(-1);
        }
    }
    

    private static void MiraLog(String sError) {
        
        try {
            File f=new File( jarPath + "log.err");
            FileWriter fw=new FileWriter(f);
            fw.write( sError );
            fw.close();
        } catch (Exception e) {
        }
    }

    
    public FirmaDigital(JFrame f) {
        // Guardamos el frame, para poder usarlo en cualquier metodo
        controllingFrame = f;

        // Creamos
        passwordField = new JPasswordField(10);
        passwordField.setActionCommand(OK);
        passwordField.addActionListener(this);

        JLabel label = new JLabel("Contraseña: ");
        label.setLabelFor(passwordField);

        JComponent buttonPane = createButtonPanel();

        JPanel textPane = new JPanel(new FlowLayout(FlowLayout.TRAILING));
        textPane.add(label);
        textPane.add(passwordField);

        add(textPane);
        add(buttonPane);
    }

    protected JComponent createButtonPanel() {
        JPanel p = new JPanel(new GridLayout(0,1));
        JButton okButton = new JButton("Aceptar");
        JButton offButton = new JButton("Cancelar");

        okButton.setActionCommand(OK);
        offButton.setActionCommand(OFF);
        okButton.addActionListener(this);
        offButton.addActionListener(this);

        p.add(okButton);
        p.add(offButton);

        return p;
    }

    public static void quitaHola() {
        File fichero = new File( jarPath + "hola.txt" );
        fichero.delete();
    }

    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();

        if (OK.equals(cmd)) { //Process the password.
            clave = passwordField.getPassword();

            passwordField.selectAll();
            resetFocus();
            Firma();
            quitaHola();
            controllingFrame.dispose();
        } else { //The user has asked for help.
            siFirmar = false;
            quitaHola();
            controllingFrame.dispose();
        }
    }


    //Must be called from the event-dispatching thread.
    protected void resetFocus() {
        passwordField.requestFocusInWindow();
    }

    private static void createAndShowGUI() {
        //Create and set up the window.
        JFrame frame = new JFrame("Firma digital");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);

        //Create and set up the content pane.
        final FirmaDigital newContentPane = new FirmaDigital(frame);
        newContentPane.setOpaque(true); //content panes must be opaque
        frame.setContentPane(newContentPane);

        //Make sure the focus goes to the right component
        //whenever the frame is initially given the focus.
        frame.addWindowListener(new WindowAdapter() {
            public void windowActivated(WindowEvent e) {
                newContentPane.resetFocus();
            }
        });

        //Display the window.
        frame.pack();
        frame.setVisible(true);
    }

    protected static void DeterminaPath() {
        CodeSource source = FirmaDigital.class.getProtectionDomain().getCodeSource();
        URL url = source.getLocation();

        String elPath = URLDecoder.decode(url.getFile());
        File f = new File(elPath);
        try {
            elPath = f.getCanonicalPath();
        } catch (IOException e) {
        }
        if (!f.isDirectory()) {
            f = new File(elPath);
            elPath = f.getParent();
        }
        jarPath = elPath + File.separator;
    }

    private static void EstamosAqui() {
        
        try {
            File f=new File( jarPath + "control.fd" );
            FileWriter fw=new FileWriter(f);
            fw.write( "x" );
            fw.close();
        } catch (Exception e) {
        }
      }

    public static void main(String[] args) {

        DeterminaPath();

        leeParametros();
        
        EstamosAqui(); // Para que sepa MGD que se ha lanzado el java correctamente
        
        if ( tipoFD.equals( "ALMACEN" ) )  {
            Firma();
            quitaHola();
        } else {
            javax.swing.SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    createAndShowGUI();
                }
            });
        }
    }
}

class KeyStoreHelperMSCAPI {

    protected KeyStore keyStore;
    protected Certificate[] certificateChain;
    protected PrivateKey privateKey;
    private Provider provider;
    
    public static String jarPath;
        
    public KeyStoreHelperMSCAPI( String JarPath ) {
        jarPath = JarPath;
        keyStore = null;
    }

    public void loadProvider() {
        try {
            provider = Security.getProvider("SunMSCAPI");
            if (provider == null) throw new ProviderException("Provider is unknown");
        } catch (ProviderException e) {
            Double javaVersion = Double.parseDouble(System
                    .getProperty("java.specification.version"));
            int javaVer = (int) Math.round(javaVersion * 10);
            if (javaVer < 16)
                LanzaError( "Es necesario que esté instalado Java v6 o superior" );
            LanzaError( "Imposible lanzar MSCAPI" );
        }
    }



    private static void LanzaError(String sError) {
        
        try {
            File fichero = new File( jarPath + "hola.txt" );
            fichero.delete();
            File f=new File( jarPath + "errorFD.err");
            FileWriter fw=new FileWriter(f);
            fw.write( sError );
            fw.close();
            System.exit(-1);
        } catch (Exception e) {
            System.exit(-1);
        }
    }

    
    public void openKeyStore() {
        try {
            keyStore = KeyStore.getInstance("Windows-MY", provider);
            keyStore.load(null, null);
        } catch (GeneralSecurityException e) {
            LanzaError( "Error desconocido intentando abrir el almacen de certificados de Windows" );
        } catch (IOException e) {
            LanzaError( "Error desconocido intentando abrir el almacen de certificados de Windows" );
        }
    }

    public Enumeration<String> getAliases() {
        try {
            return (Enumeration<String>) keyStore.aliases();
        } catch (KeyStoreException e) {
            LanzaError( "An unknown error accoured while listing the available "
                            + "aliases from your personal Microosft Windows certificate store" );
            return null;
        }
    }

    public Certificate[] getCertificateChain(String alias)
            {
        try {
            if (!keyStore.containsAlias(alias))
                LanzaError( "No se ha podido abrir el alias \"" + alias + "\"");
        } catch (KeyStoreException e) {
                LanzaError( "Error desconocido intentando leer el almacen de certificados de Windows" );
        }
        try {
            return keyStore.getCertificateChain(alias);
        } catch (KeyStoreException e) {
                LanzaError( "Error desconocido intentando leer el almacen de certificados de Windows" );
            return null;
        }
    }

    public void loadAlias(String alias ) {//, char[] clave) {
        try {
            if (!keyStore.containsAlias(alias))
                LanzaError( "No se ha podido abrir el alias \"" + alias + "\"");
        } catch (KeyStoreException e) {
                LanzaError( "No se ha podido abrir el alias \"" + alias + "\"");
        }
        try {
            privateKey = (PrivateKey) keyStore.getKey(alias, null ); //clave );
            certificateChain = keyStore.getCertificateChain(alias);
        } catch (GeneralSecurityException e) {
                LanzaError( "No se ha podido abrir el alias \"" + alias + "\"");
        }
    }

    public Certificate getCertificate(String alias) {
        try {
            return keyStore.getCertificate(alias);
        } catch (KeyStoreException e) {
                LanzaError( "No se ha podido abrir el alias \"" + alias + "\"");
            return null;
        }
    }

       public Certificate[] getCertificateChain() {
        return certificateChain;
    }

    public PrivateKey getPrivateKey() {
        return privateKey;
    };


}

