all: run.ipynb

clean:
	rm run.ipynb

SNIPPETS := ../fabric-snippets/fab-config.md ../fabric-snippets/reserve-resources.md ../fabric-snippets/extend.md ../fabric-snippets/configure-resources.md ../fabric-snippets/offload-off.md ../fabric-snippets/draw-topo-detailed-labels.md ../fabric-snippets/log-in.md ../fabric-snippets/delete-slice.md
run.ipynb: $(SNIPPETS) custom-snippets/intro.md custom-snippets/exp-define.md custom-snippets/exp-validate.md custom-snippets/exp-configure-network.md custom-snippets/exp-1b.md  custom-snippets/exp-1c.md 
	pandoc --wrap=none \
                -i custom-snippets/intro.md \
		../fabric-snippets/fab-config.md \
		custom-snippets/exp-define.md \
                ../fabric-snippets/reserve-resources.md \
				 ../fabric-snippets/extend.md \
		../fabric-snippets/configure-resources.md \
		../fabric-snippets/offload-off.md  \
		custom-snippets/exp-validate.md \
		../fabric-snippets/draw-topo-detailed-labels.md \
		../fabric-snippets/log-in.md \
		custom-snippets/exp-configure-network.md \
		custom-snippets/exp-1b.md \
		custom-snippets/exp-1c.md \
		../fabric-snippets/delete-slice.md \
                -o run.ipynb  
